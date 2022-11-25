# **danc_python** - диаграммы как код

Diagram As Native Language on Python - work with diagrams as code with a help of Python

## Еще один способ работать с диаграммами как кодом.

Вы можете:

- Описать диаграмму в виде текста или в виде Python кода
- Можете добавить заголовок, описание, теги для поиска и т.п.
- Разместить в структуре папок на коммпьютере и отобразить их через WEB доступ
- Отслеживать версии и изменения с помощью Git
- Генерировать SVG файлы
- Генерировать URL ссылки для встраивания на ваши страницы
- Открывать в браузере Ваши файлы диаграмм
- Работать с диаграммами с помощью Jupyter Lab
- Создать с помощью Jupyter Lab каталог диаграм или даже - электронный альбом
- При использовании Python или Jupyter версий Вы можете интегрировать Ваши диаграммы в информационную систему вашего предприятия. Модифицировать их по шаблонам, подгружать внешние данные

Генерация SVG производится через сервер [kroki.io](https://kroki.io/), в результате чего вам доступны более 20 типов систем диаграмм, в том числе:

 - BlockDiag ("blockdiag")
 - BPMN ("bpmn")
 - Bytefield ("bytefield")
 - SeqDiag ("seqdiag")
 - ActDiag ("actdiag")
 - NwDiag ("nwdiag")
 - PacketDiag ("packetdiag")
 - RackDiag ("rackdiag")
 - C4 with PlantUML ("c4plantuml")
 - Ditaa ("ditaa")
 - Erd ("erd")
 - Excalidraw ("excalidraw")
 - GraphViz ("graphviz")
 - Mermaid ("mermaid")
 - Nomnoml ("nomnoml")
 - Pikchr ("pikchr")
 - PlantUML ("plantuml")
 - Structurizr ("structurizr")
 - Svgbob ("svgbob")
 - Vega ("vega")
 - Vega-Lite ("vegalite")
 - WaveDrom ("wavedrom")
 
(https://kroki.io/#support)

### Главные плюсы сейчас:

- Минимальные требования к зависимостями: текстовый редактор и Python.
- Использование стандартных средств типа Git.
- Возможность генерировать диаграммы на более 20 языках [Типы диаграмм](https://kroki.io/#support) 
- Возможно втраивать в корпоративную систему предприятия.
- При использовании Jupyter Lab (https://docs.jupyter.org/en/latest/) можно реализовать "из коробки" редактирование диаграм через WEB, создание комплексных документов с диаграммами, создание библиотек, альюбомов и электронных книг с описаниями и диаграммами.

## Возможности сейчас:

**Альфа версия. Концептуальный проект**

Текущая версия скорее концептуальный проект. Однако всеми имеющимися возможностями можно пользоватся в реальной раоте. 
Предлагаемый в комплекте WEB сервер - специально сделан минимальным, на стандартных средствах Python что бы уменьшить "на стартте" зависимость от зависимостей. Тем не мение, его можно использовать внутри корпоративных сетей как срество просмотра. Но если "тема пойдет" - лучше сервер реализовать на боле серьезных средствах типа Django, Flask и т.п. Можно организовать API доступ к каталогу диаграмм и к созданным SVG, орагнзовать кеширование сгенерированных SVG.

В файлах модулей включен параметр `TAGS` -- в текущей версии никак не используется, включен как образец возможностей.

### Генерация svg по тексту диаграммы и просмотр в браузере

Просмотр текстового файла. Примеры файлов включены в репозитарий в каталоге `code/data`

Команды выполняются в каталоге `/code` от корня проекта.

Пример - UMLet:

	python3 view_file.py umlet ./data/NativeLangDiagramStruct.uxf

Пример - structurizr:

	python3 view_file.py structurizr ./data/subdir/aws.dsl

Таким образом можно запускать тексты любых диаграмм, поддерживаемых системой. Тип диаграммы указывается в первом параметре, файл - во втором. Файл может быть размещен где угодно.

Просмотр специального python файла с кодом диаграммы:

	python view_file.py py ./data/marm_example2.py

	python view_file.py py ./data/subdir/aws_example.py

Первый параметр - обозначение "py"

Питон файлы диаграмм так же могут размещатся где угодно.

Режим автопросмотра в браузере не доступен при запуске из Docker. В этом варианте можно использовать генерацию URL или получение svg


### Генерация svg по тексту диаграммы и сохраненеи в файл

Аналогично открытию в браузере, но добавляется параметр `-o <файл для выгрузки>`

	python3 view_file.py -o my.svg umlet ./data/NativeLangDiagramStruct.uxf

	python3 view_file.py -o my.svg structurizr ./data/subdir/aws.dsl

	python view_file.py -o my.svg py ./data/marm_example2.py

	python view_file.py -o my.svg py ./data/subdir/aws_example.py

При запуске через Docker (docker-compose):

Команды нужно выполнять в корне проекта.

	docker-compose run web svg -o my.svg umlet ./data/NativeLangDiagramStruct.uxf

	docker-compose run web svg -o my.svg structurizr ./data/subdir/aws.dsl

	docker-compose run web svg -o my.svg py ./data/marm_example2.py

	docker-compose run web svg -o my.svg py ./data/subdir/aws_example.py

При этом файлы могут быть размещены только в подкаталоге `data` проекта, так как контейнер Докера не имеет доступа к другим местам. Файл с svg будет сгенерирован относительно корня проекта. Можно подключить другие тома - но это уже другая история.

Пользовательские диаграммы можно размещать в каталоге `code/data/user` и в подкаталогах, тогда можно будет открывать их через каталог в браузере (см. ниже) и не будет засорятся Git проекта.


### Генерация url svg по тексту диаграммы для включения на страницы и в документы

Аналогично открытию в браузере, но добавляется параметр `-u`

	python3 view_file.py -u umlet ./data/NativeLangDiagramStruct.uxf

	python3 view_file.py -u structurizr ./data/subdir/aws.dsl

	python view_file.py -u py ./data/marm_example2.py

	python view_file.py -u py ./data/subdir/aws_example.py

При запуске через Docker (docker-compose):

	docker-compose run web url umlet ./data/NativeLangDiagramStruct.uxf

	docker-compose run web url structurizr ./data/subdir/aws.dsl

	docker-compose run web url py ./data/marm_example2.py

	docker-compose run web url py ./data/subdir/aws_example.py


### Организация каталога диаграмм с поддержкой описания

Предусмотрен локальный веб сервер, который организует просмотр каталога и подкаталогов от `code/data`. Отображает файлы доступных форматов. Для файлов `.py` читает и отображает метаинформацию.

сейчас реализация сделана минимальной,стандартными средствами Python, по этому и выглядит просто, и категорически НЕ желательно запускать во внещний доступ.

Для запуска выполнить команду:

	python3 serve.py

Программа запустится и будет отрабатывать web запросы.

Открыть браузер и зайти: `http://127.0.0.1:8080`


Для запуска в Docker:

	docker-compose up

Или

	docker-compose run web serve

Далее так же открыть браузер и зайти: `http://127.0.0.1:8080`


### Использование в качестве библиотеки

В каталоге code/danc_python определены классы и функции для работы с диаграммами. Можно включить катаолг `danc_python` в свой проект и использовать. Возможности описаны в коментариях и примерах утилит.

Пока размещение в PyPi не сделано, пользоватся толко так.

### Использование в Juputer:

В комплекте есть 2 образца:

- `example1.ipynb` -- пример работы с кодом в ноутбуке.
- `example_module.ipymb` -- пример работы из ноутбука с файлами - моулями диаграм.

## Установка и запуск:

Для установки достаточно скачать и развернуть репозитарий проекта.

### При наличии Python

Провет работает с сипользванием Python версии 3.6 и старше. Если использовать Linux, то Python присутствует как системная утилита.

Для скачивания svg нужно установить зависимость `requests` - диблиотека для работы с интернет запросами. В корне проекта выполнить:

	pip3 install -r ./code/requirements.txt

Далее просто запускать команды из каталога `code` проекта.


### При использовании Docker

Для тех, у кого не установлен Python, но установлен Docker и Docker-compose, можно запустить через них. Для этого в корне проекта нужно собрать контейнер командой:

	docker-compose build

И можно пользоватся.



## Форматы файлов.

### Диаграмма в python файле

Диаграмма может быть размещена в специально орагнизованном python файле. "Специальноть" его заключается в определении нескольких констант и функции генерации (или константы с кодом).
Этот файл загружается и выполняется системой. Так как эо обычный python - можно использовать все возможности языка.

Пример кода:

```python
"""
	Диаграмма в модуле
"""

DIAGRAM_TYPE = "mermaid.state"
TITLE = "Mermaid пример 1"
DESCRIPTION = "Для демонстрации концепции с использованием Mermaid"
TAGS=["mermaid", "example", "py"]
DETAIL="""
А тут большое и толстое описание всего
"""

def draw(d):
    d.l(None, "ListTable")
    d.l("ListTable", "InitObj", "NewObj")
    d.l("ListTable", "LoadObj", "EditObj")
    d.l("InitObj", "ShowModal")
    d.l("LoadObj", "ShowModal")
    d.l("LoadObj", "EditModal")
    d.l("EditModal", "StoreDetail", "Accept")
    if_state = d.iif()
    d.l("StoreDetail", if_state)
    d.l(if_state, "CloseModal", "success")
    d.l(if_state, "ShowErrors", "error")
    d.l("ShowErrors", "EditModal")
    d.l("EditModal", "CloseModal", "Cancel")
    d.l("EditModal", "CloseModal", "Error")
    d.l("CloseModal", "RefreshList")
    d.l("RefreshList", "ListTable")
    d.l("ListTable", None)

```

Это как раз пример описания диаграммы mermaid state diagramm с помощью python вызовов. Более сложные примеры в каталоге code/data.

В файле нужно определить:

`DIAGRAM_TYPE` -- строка, тип диаграммы.

`TITLE` -- строка, "человеческое" название диаграммы. Будет отображатся в браузере вместо имени файла.

`DESCRIPTION` -- строка, описание диаграммы.

`TAGS` -- список строк - тегов. Пока не используется.

`DETAIL` -- Более подробное описание диаграммы. Будет отображено в браузере на странице диаграммы. Можно использовать html. 

`def draw(d):` -- функция, которая генерирует диаграмму. Должна быть обязательно, или должна быть определена константа `CODE` -- текст кода диаграммы на ее собствнном языке.


### Диаграмма в текстовом файле

Можно разместить текст кода диаграммы на ее собственном языке в отдельный текстовый файл и открывать его утилитой из командной строки.

Так как расширения файлов неоднозначноопределяют тип, каталог в браузере не позволяет открывать просто файлы. 
Для работы из браузерного каталога диаграммы нужно разместить в питон файлах в блоке `CODE`, и определеить метаинформацию.
 

