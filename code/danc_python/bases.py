"""
"""

import webbrowser
import sys, os
import base64
import zlib
import traceback


__all__=["Diagram", "DrawItem", "DrawBase", "list_dir", "load_module"]


KROKI = "https://kroki.io/{type_name}/{render_type}/{hash}"

DIR_DESCRIPTION_FILE = "__description__.py"


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
            return DrawBase(draw_type)
        else:
            return dt(draw_type)


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


class DICode(DrawItem):

    def __init__(self, txt):
        """
        """
        self.base._set_code(txt)


class DrawBase:
    """
        Предоставляет методы генерации диаграмы, собирает результат
    """

    def __init__(self, type_name):
        """
        """
        self._type_name = type_name
        self._plain_code = None
        self._buffer = []
        self._cur_level = 0
        self._indent_size = 4
        self._cur_id = 0

    @property
    def code(self):
        return self._prep_item(DICode)

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
    base_dir, dir_path = _dir_clear(base_dir, dir_path)
    dirname = base_dir + dir_path
    res = []
    dir_descr = None
    with os.scandir(dirname) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue
            if entry.name==DIR_DESCRIPTION_FILE:
                dir_descr = _proc_dir_descr(base_dir, dir_path, entry)
                continue
            if entry.name.startswith('_'):
                continue
            if entry.name.endswith(".py"):
                itm = _proc_module(base_dir, dir_path, entry)
            elif entry.is_file():
                itm = dict(
                    name=dirname + "/" + entry.name, 
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
                itm = dict(
                    name=dirname + "/" + entry.name,
                    title=entry.name, 
                    description="", 
                    detail=None, 
                    tags=[], 
                    dia_type=None, 
                    is_dir=True,
                    link=dir_path + "/" + entry.name, 
                    )
            res.append(itm)

    return res


def load_module(in_file):
    """
        Загружает и выполняет модуль. Возвращает словарь с объектами модуля.
    """
    if isinstance(in_file, str):
        with open(in_file, 'r', encoding="utf-8") as fm:
            buf = "".join([l for l in fm])
            module_name = in_file
    else:
        buf = in_file.read()
        module_name = "<string>"

    mc = compile(buf, module_name, "exec")
    module = {}
    exec(mc, module)

    return module


def _proc_dir_descr(base_dir, dir_path, entry):
    pass

def _proc_module(base_dir, dir_path, entry):
    base_dir, dir_path = _dir_clear(base_dir, dir_path)

    in_file = base_dir + dir_path +"/" + entry.name 

    itm = dict(
        name=in_file, 
        title=entry.name,
        link=dir_path + "/" + entry.name,
        description="", 
        detail="", 
        tags=[], 
        dia_type=None, 
        is_dir=False,
        do_link=True,
        )
    
    try:
        module = load_module(in_file)
    except Exception as e:
        traceback.print_exc()
        itm["link"] = None
        itm["description"] = "== ошибка иморта ==",
        return itm
    itm["title"] = module.get("TITLE", entry.name)
    itm["description"] = module.get("DESCRIPTION", "")
    itm["detail"] = module.get("DETAIL", "")

    return itm

