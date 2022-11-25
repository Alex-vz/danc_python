"""
"""

from pathlib import Path

import webbrowser
import sys, os
import base64
import zlib
import traceback


__all__=["Diagram", "DrawItem", "DrawBase", "DiaModule", "list_dir", "load_module"]


KROKI = "https://kroki.io/{type_name}/{render_type}/{hash}"

DIR_DESCRIPTION_FILE = "__description__.py"

DIAGRAM_TYPES = {
    "blockdiag":"BlockDiag",
    "bpmn": "BPMN",
    "bytefield": "Bytefield",
    "seqdiag": "SeqDiag",
    "actdiag": "ActDiag",
    "nwdiag": "NwDiag",
    "packetdiag": "PacketDiag",
    "rackdiag": "RackDiag",
    "c4plantuml": "C4 with PlantUML",
    "ditaa": "Ditaa",
    "erd": "Erd",
    "excalidraw": "Excalidraw",
    "graphviz": "GraphViz",
    "mermaid": "Mermaid",
    "nomnoml": "Nomnoml",
    "pikchr": "Pikchr",
    "plantuml": "PlantUML",
    "structurizr": "Structurizr",
    "svgbob": "Svgbob",
    "vega": "Vega",
    "vegalite": "Vega-Lite",
    "wavedrom": "WaveDrom",
}


class Diagram:
    """
        Базовый клас диаграм
    """
    _dia_types = {}

    @classmethod
    def register(cls, name, class_obj):
        cls._dia_types[name] = class_obj

    def __init__(self):
        """
        """

    def perp_url(self, draw, render_type="svg"):
        code=draw._get_code()
        print(code)
        c = self.calc_code(draw._get_code())
        return KROKI.format(type_name=draw._type_name, render_type=render_type, hash=c)

    def open_in_browser(self, draw):
        """
        """
        webbrowser.open(self.perp_url(draw))

    def render_to_file(self, draw, fname, render_type="svg"):
        import requests
        r = requests.get(self.perp_url(draw), stream=True)
        if r.status_code == 200:
            with open(fname, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print(r.status_code)
        r.close()

    def get_svg(self, draw):
        import requests
        r = requests.get(self.perp_url(draw), stream=True)
        if r.status_code == 200:
            res = bytearray()
            for chunk in r.iter_content(1024):
                res += chunk
            r.close()
        else:
            raise Exception(f"Status: {r.status_code}")
        return res

    def calc_code(self, txt):
        #import sys; import base64; import zlib; print(base64.urlsafe_b64encode(zlib.compress(sys.stdin.read().encode('utf-8'), 9)).decode('ascii'))
        res = base64.urlsafe_b64encode(zlib.compress(txt.encode('utf-8'), 9)).decode('ascii')
        return res

    def init_draw(self, draw_type):
        """
            Возвращает объект "рисовальщика" соотвествующего типа
        """
        dt = self._dia_types.get(draw_type)
        if not dt:
            return DrawBase(draw_type, self)
        else:
            return dt(draw_type, self)

    def display(self, draw, display=None):
        """
            displays SVG in Jupytre notebook
        """
        from IPython import display
        return display.SVG(self.get_svg(draw).decode("utf-8"))

    @classmethod
    def display_code(cls, draw_type, code):
        """
            Displays svg from code of type draw_type
        """
        obj = cls()
        d = obj.init_draw(draw_type)
        d.code(code)
        return d


class DrawItem:
    base = None
    prefix = "sate"

    def __init__(self, sid=None):
        """
        """
        if not sid:
            self.state_id=self.base._get_id(prefix=self.prefix)
        else:
            self.state_id=sid


class DrawBase:
    """
        Предоставляет методы генерации диаграмы, собирает результат
    """

    def __init__(self, type_name, diagram):
        """
        """
        self._type_name = type_name
        self._plain_code = None
        self._buffer = []
        self._cur_level = 0
        self._indent_size = 4
        self._cur_id = 0
        self._diagram = diagram

    @property
    def code_0(self):
        return self._prep_item(DICode)

    @classmethod
    def register_item(cls, name, shortname=None):

        class _ItemDescr:
            def __init__(self, itm_cls):
                self.itm_cls=itm_cls
            def __get__(self, instance, owner):
                if instance:
                    return instance._prep_item(self.itm_cls)
                else:
                    return self.itm_cls

        def func(act_cls):
            setattr(cls, name, _ItemDescr(act_cls))
            if shortname:
                setattr(cls, shortname, _ItemDescr(act_cls))
            return act_cls

        return func

    def _prep_item(self, item_class):
        return type(item_class.__name__, (item_class,), {"base":self})

    def _set_code(self, code_text):
        self._plain_code=code_text

    def _get_id(self, prefix=None):
        if prefix is None:
            prefix = "state"
        self._cur_id += 1
        return "{}_{}".format(prefix, self._cur_id)

    def _add(self, code_line):
        """
            Добавить строку кода в буфер
        """
        self._buffer.append(self._set_indent(code_line))

    def _set_indent(self, code_line):
        if self._cur_level:
            return " "*(self._cur_level*self._indent_size) + code_line
        else:
            return code_line

    def _inc_level(self):
        """
        """
        self._cur_level += 1

    def _dec_level(self):
        """
        """
        if self._cur_level:
            self._cur_level -= 1

    def _get_code(self):
        if self._plain_code:
            return self._plain_code
        return "\n".join(self._buffer)

    def _repr_svg_(self):
        """
        """
        return self._diagram.get_svg(self).decode("utf-8")


@DrawBase.register_item("code")
class DICode(DrawItem):
    """
        Элемент, содержащий код на языке диаграммы.
        ??Если присутствует то определяет всю диаграмму, игнорируя остальное
    """

    def __init__(self, txt):
        """
        """
        self.base._set_code(txt)


@DrawBase.register_item("template", "tmpl")
class DITemplate(DrawItem):
    """
        Элемент, содержащий код с расшираяемыми элементами шаблона.
        context::dict -- словарь данных, используемых в качестве конекста рендеринга.
        tmpl_lang::str -- идентификатор шаблонизатора, установленного в системе
        tmpl_id::str -- идентификатор шаблоного субблока. Для включения в главный шаблон.
            если задан - то самостоятельно не отображается, только через мастершаблон.
        sid::str -- идентификатор блока в схеме
    """

    def __init__(self, txt, context=None, tmpl_lang=None, tmpl_id=None, sid=None):
        """
        """
        pass


def _dir_clear(base_dir, dir_path):
    base_dir = base_dir.rstrip("/")
    if not dir_path or dir_path=="/":
        dir_path = ""
    elif not dir_path.startswith("/"):
        dir_path = "/"+dir_path
    return base_dir, dir_path


def list_dir(base_dir, dir_path):
    """
        Возвращает список файлов в куказанном каталоге.
        Модули python пытается импортировать и считать описание.
        Первый элемент в списке - описание самого каталога.

        Элементы списка: {name, title, dscription, detail, tags, dia_type, is_dir, do_link}
    """
    #base_dir, dir_path = _dir_clear(base_dir, dir_path)
    #dirname = base_dir + dir_path

    base_dir = Path(base_dir) 
    dir_path = Path("./"+dir_path)
    dirname = base_dir / dir_path

    res = []
    dirs = []
    dir_descr = None
    for entry in dirname.iterdir():
        if str(entry).startswith('.'):
            continue
        if entry.name==DIR_DESCRIPTION_FILE:
            dir_descr = _proc_dir_descr(base_dir, entry)
            continue
        if entry.name.startswith('_'):
            continue
        if entry.suffix == ".py":
            itm = _proc_module(base_dir, entry)
        elif entry.is_file():
            itm = dict(
                name=str(entry), 
                title=entry.name, 
                description="", 
                detail=None, 
                tags=[], 
                dia_type=None, 
                is_dir=False,
                #link=dir_path + "/" + entry.name, 
                link=None, 
                )
        else:
            itm = _proc_subdir_descr(base_dir, entry)
            """
            itm = dict(
                name=str(entry),
                title=entry.name, 
                description="", 
                detail=None, 
                tags=[], 
                dia_type=None, 
                is_dir=True,
                link="/"+str(entry.relative_to(base_dir)), 
                )
            """
        if itm["is_dir"]:
            dirs.append(itm)
        else:
            res.append(itm)

    return dirs+res, dir_descr


def load_module(in_file):
    """
        Загружает и выполняет модуль. Возвращает словарь с объектами модуля.
    """
    if isinstance(in_file, str):
        in_file = Path(in_file)
    if isinstance(in_file, Path):
        with in_file.open('r', encoding="utf-8") as fm:
            buf = "".join([l for l in fm])
            module_name = in_file
    else:
        buf = in_file.read()
        module_name = "<string>"

    mc = compile(buf, module_name, "exec")
    module = {}
    exec(mc, module)

    return module


class EModuleLoadError(Exception):
    pass


class EUnknownType(Exception):
    pass


class ENoDiagramCode(Exception):
    pass


class EDiagramProcessError(Exception):
    pass


DEFAULT_TEMPLATE = """
    <h1>{title}</h1>
    <div>{description}</div>
    <div>
        <img src="{image_url}">
    </div>
    <div>{detail}</div>
"""

class DiaModule:
    """
        Работа с python модулем диаграмм.
    """

    def __init__(self, module_name, raise_errors=True, template=None):
        """
            Загружает модуль из файла module_name
        """

        self.error = None
        self.raise_errors = raise_errors
        self.diagram = None
        self.draw = None
        self.module_name = module_name
        self.module = load_module(module_name)
        if not template:
            self.template = DEFAULT_TEMPLATE
        else:
            self.template = template
        try:
            self.module = load_module(module_name)
        except Exception as e:
            traceback.print_exc()
            if raise_errors:
                raise EModuleLoadError(str(e))
            else:
                self.error = "Ошибка загрузки модуля"
                return

        self.dtype = self.module.get("DIAGRAM_TYPE")
        if not self.dtype:
            if raise_errors:
                raise EUnknownType("Unknown diagram type")
            else:
                self.error = "Не задан тип диаграммы"
                return

        self.draw_func = self.module.get("draw")
        self.code_block = self.module.get("CODE")
        if not (self.draw_func or self.code_block):
            if raise_errors:
                raise ENoDiagramCode("Unknown diagram type")
            else:
                self.error = "Не задан код диаграммы"
                return

    def get_diagram(self):
        """
            Генерирует диаграмму по данным модуля
        """

        self.diagram = Diagram()
        try:
            d = self.diagram.init_draw(self.dtype)
            if self.draw_func:
                self.draw_func(d)
            else:
                d.code(self.code_block)
        except Exception as e:
            traceback.print_exc()
            if raise_errors:
                raise EDiagramProcessError(str(e))
            else:
                self.error = "Ошибка при генерации: {}".format(str(e))
                return

        self.draw = d
        return self.draw

    @property
    def title(self):
        return self.module.get("TITLE", self.module_name)

    @property
    def description(self):
        return self.module.get("DESCRIPTION", "")

    @property
    def detail(self):
        return self.module.get("DETAIL", "")

    @property
    def image_url(self):
        if self.error:
            return None
        if not self.draw:
            self.get_diagram()
        if self.error:
            return None
        return self.diagram.perp_url(self.draw)

    @property
    def svg(self):
        """
            Возвращает код SVG для дальнейшего использования
        """
        if self.error:
            return None
        if not self.draw:
            self.get_diagram()
        if self.error:
            return None
        return self.diagram.get_svg(self.draw).decode("utf-8")

    def display_svg(self):
        """
            Отобразить в Jupyter только картинку (svg) диаграммы
        """
        if self.error:
            return self.error
        svg = self.svg
        if self.error:
            return self.error
        from IPython import display
        return display.SVG(svg)

    def _repr_html_(self):
        self.get_diagram()
        if self.error:
            return '<div style="color:red;fomt-weight:bold;">Ошибка при генерации</div>'
        res = self.template.format(
            title=self.title,
            description=self.description,
            image_url=self.image_url,
            detail=self.detail)
        return res


def _proc_dir_descr(base_dir, entry):
    itm = dict(
        name=str(entry), 
        title=entry.name,
        link="/"+str(entry.relative_to(base_dir)),
        description="", 
        detail="", 
        tags=[], 
        dia_type=None, 
        is_dir=False,
        )
    
    try:
        module = load_module(entry)
    except Exception as e:
        traceback.print_exc()
        itm["link"] = None
        itm["description"] = "== ошибка иморта ==",
        return itm
    itm["title"] = module.get("TITLE", entry.name)
    itm["description"] = module.get("DESCRIPTION", "")
    itm["detail"] = module.get("DETAIL", "")

    return itm


def _proc_subdir_descr(base_dir, entry):
    entry_d = entry / Path(DIR_DESCRIPTION_FILE)
    itm = dict(
        name=str(entry), 
        title=entry.name,
        link="/"+str(entry.relative_to(base_dir)),
        description="", 
        detail="", 
        tags=[], 
        dia_type=None, 
        is_dir=True,
        )
    if entry_d.exists():
        try:
            module = load_module(entry_d)
        except Exception as e:
            traceback.print_exc()
            itm["link"] = None
            itm["description"] = "== ошибка иморта ==",
            return itm
        itm["title"] = module.get("TITLE", entry.name)
        itm["description"] = module.get("DESCRIPTION", "")
        itm["detail"] = module.get("DETAIL", "")

    return itm


def _proc_module(base_dir, entry):
    """
        base_dir, entry::Path
    """
    #base_dir, dir_path = _dir_clear(base_dir, dir_path)

    #in_file = base_dir + dir_path +"/" + entry.name 


    itm = dict(
        name=str(entry), 
        title=entry.name,
        link="/"+str(entry.relative_to(base_dir)),
        description="", 
        detail="", 
        tags=[], 
        dia_type=None, 
        is_dir=False,
        )
    
    try:
        module = load_module(entry)
    except Exception as e:
        traceback.print_exc()
        itm["link"] = None
        itm["description"] = "== ошибка иморта ==",
        return itm
    itm["title"] = module.get("TITLE", entry.name)
    itm["description"] = module.get("DESCRIPTION", "")
    itm["detail"] = module.get("DETAIL", "")

    return itm

