## Документация

Фреймворк предназначен для создания чат-ботов Telegram на базе популярного веб-фреймворка Django. Он включает
в себя собственную стейт-машину и инструменты для работы с вебхуками.

## Быстрый старт

Далее приводится порядок действий по созданию простейшего эхо-бота, как начальную точку создания любого бота.
Предполагается, что вы владеете либо имеете достаточное представление по работе с [Django](https://docs.djangoproject.com/en/4.2/), [Poetry](https://python-poetry.org/docs/), [Pydantic](https://docs.pydantic.dev/1.10/), [Tg API](https://core.telegram.org/bots/api)

### Создайте новый проект Poetry:

`poetry new django-bot-project --name django_project`

`cd django-bot-project`

### В файле pyproject.toml укажите следующие зависимости:

```toml
[tool.poetry]
name = "django-project"
version = "0.1.0"
description = ""
authors = ["YourName <your_mail@your_domain.ru>"]
readme = "README.md"
packages = [{include = "django_project"}]

[tool.poetry.dependencies]
python = "^3.11"
django = "4.2.4"
django-tg-bot-framework = {git = "https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/django_tg_bot_framework.git", rev = "c504a47496823cd7715f8d4d4df9915a48cbb5c3"}
rollbar = "0.16.3"
django-debug-toolbar = "4.2.0"
pydantic = {extras = ["dotenv"], version = "1.10.8"}


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Установите зависимости в виртуальное окружение:
`poetry install`

### После этого создайте новый проект django:
`cd django_project`

`poetry run django-admin startproject django_tg_bot`

### Корректировка вложенности директорий

Поскольку Django рассчитан на разработку крупных проектов, то его структура по умолчанию обладает соответствующей вложенностью.
Чтобы исключить излишнюю вложенность папок, переместите содержимое вложенной папки проекта `django_tg_bot` в папку проекта `django_project`, предварительно переименовав родительскую папку `django_tg_bot`.
Создайте папку `static` в корне вашего проекта.
В итоге дерево папок проекта должно выглядеть следующим образом:
```
django-bot-project/
├── django_project
│   ├── django_tg_bot
│   └── static
│  
└── tests

```

### Создайте приложение tg_bot:
`./manage.py startapp tg_bot`

В итоге дерево папок проекта должно выглядеть следующим образом:
```
django-bot-project/
├── django_project
│   ├── django_tg_bot
│   ├── static
│   └── tg_bot
│       └── migrations
└── tests


### В корне проекта django создайте файл `.env` с переменными окружения:

```dotenv
TG__BOT_TOKEN=<Токен от вашего бота>
TG__WEBHOOK_TOKEN='webhook_token'
DJ__SECRET_KEY='django-insecure-zpkx0hyd!bxm2c0z$9-gt@hq5k+ssfs3+pho2gd)$(e-3gbbq1it@='
DJ__DEBUG='true'
DJ__ALLOWED_HOSTS='127.0.0.1, localhost, .ngrok-free.app'
DJ__CSRF_TRUSTED_ORIGINS='https://*.ngrok-free.app'
WEBAPP_ROOT_URL=http://127.0.0.1:8000
ENABLE_DEBUG_TOOLBAR=true
ENABLE_MEDIA_FILES_SERVING=true
TG_BOT_LOGGING_LEVEL=DEBUG
DJANGO_TG_BOT_FRAMEWORK_LOGGING_LEVEL=DEBUG
DJANGO_TG_BOT_FRAMEWORK_MOCK_MESSAGES_ENABLED=true
```

### Там же, в корне проекта создайте файл `env_settings.py`с описанием типов переменных окружения на основе моделей Pydantic:
Содержимое файла см. в репозитории примера бота -> [env_settings.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/env_settings.py)

### Выполните настройки в файле settings.py: пропишите необходимые переменные, подключите приложения
Содержимое файла см. в репозитории примера бота -> [settings.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/django_tg_bot/settings.py)


### Задайте urlpatterns для проекта django в файле `django_tg_bot/urls.py`:
Содержимое файла см. в репозитории примера бота -> [django_tg_bot/urls.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/django_tg_bot/urls.py)

### Задайте urlpatterns для приложения tg_bot в файле `tg_bot/urls.py`:
Содержимое файла см. в репозитории примера бота -> (tg_bot/urls.py)[https://github.com/Sergryap/django-bot-project/blob/main/django_project/tg_bot/urls.py]

### Для приложения tg_bot cоздайте модели для базы данных в файле `tg_bot/models.py`
Содержимое файла см. в репозитории примера бота -> [tg_bot/models.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/tg_bot/models.py)

### В короне пакета приложения tg_bot создайте файл `state_machine_runners.py`
Данный файл необходим для переключения между состояниями бота и в дальнейших версиях будет перенесен во фреймворк.

Содержимое файла см. в репозитории примера бота -> [state_machine_runners.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/tg_bot/state_machine_runners.py)

### В корне пакета приложения tg_bot создайте файл `states.py`
Данный файл содержит в себе основную логику работы бота и состоит из отдельных состояний (states), описанных в виде классов, и связанных между собой.

Для создания простейшего эхо-бота файл [states.py](https://github.com/Sergryap/django-bot-project/blob/main/django_project/tg_bot/states.py) может выглядеть так:

```python
from typing import Optional
from django_tg_bot_framework import BaseState, Router, InteractiveState
from tg_api import Message, SendMessageRequest


router = Router()


@router.register('/')
class FirstUserMessageState(InteractiveState):
    """Состояние используется для обработки самого первого сообщения пользователя боту.

    Текст стартового сообщения от пользователя игнорируется, а бот переключается в
    следующий стейт, где уже отправит пользователю приветственное сообщение.

    Если вы хотите перекинуть бота в начало диалога -- на "стартовый экран" --, то используйте другое
    состояние с приветственным сообщением. Это нужно только для обработки первого сообщения от пользователя.
    """

    def react_on_message(self, message: Message) -> BaseState | None:
        SendMessageRequest(
            chat_id=message.chat.id,
            text='Вас приветствует ваш первый Эхо-бот'
        ).send()
        return router.locate('/welcome/')


@router.register('/welcome/')
class EchoBotState(InteractiveState):

    def enter_state(self) -> Optional['BaseState']:
        return

    def react_on_message(self, message: Message) -> BaseState | None:
        SendMessageRequest(
            chat_id=message.chat.id,
            text=message.text,
        ).send()
        return router.locate('/welcome/')
```
### Создайте миграции и примените их:
`./manage.py makemigrations`

`./manage.py migrate`

### По завершению настроек структура дерева проекта должно выглядеть следующим образом:

```
django-bot-project/
├── django_project
│   ├── db.sqlite3
│   ├── django_tg_bot
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── env_settings.py
│   ├── .env
│   ├── __init__.py
│   ├── manage.py
│   ├── static
│   └── tg_bot
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── state_machine_runners.py
│       ├── states.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

### Зарегистрируйте webhook для получения обновлений от tg api:

Для подключения к Telegram API нужно зарегистрировать вебхук-сервер, а для этого понадобится публичный адрес.
Получить его можно с помощью [https://ngrok.com/](https://ngrok.com/).<br>
Перейдите по ссылке и пройдите регистрацию.
На сайте будут подробные инструкции по установке **ngrok** на вашу операционную систему.<br>

Чтобы получить публичный IP адрес для вашей разработческой машины сначала авторизуйте ngrok с помощью команды
`ngrok config add-authtoken`, как это указано в личном кабинете на сайте [https://ngrok.com/](https://ngrok.com/), а затем запустите
команду:

```shell
$ ngrok http 8000
Session Status                online
Account                       Евгений Евсеев (Plan: Free)
Version                       3.3.1
Region                        Europe (eu)
Latency                       48ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://3b1d-95-70-162-108.ngrok-free.app -> http://127.0.0.1:8000
Connections                   ttl     opn     rt1     rt5     p50     p90
                              19      0       0.00    0.00    0.04    0.10
```

Ngrok сообщит вам публичный адрес и начнём пробрасывать входящий трафик на порт 8000 вашего локального компьютера.
Обратите внимание, что бесплатная версия Ngrok предоставляет временные адреса, которые меняются при каждом запуске `ngrok`. Лучше
не выключайте `ngrok` во время работы с сайтом.

Теперь осталось сообщить серверу телеграм, о нашем webhook-сервере:

```shell
$ # Замените `https://example.ngrok-free.app` на полученный от ngrok публичный адрес
$ PUBLIC_URL="https://example.ngrok-free.app"
$ # Замените `1613441681:example` на токен вашего телеграм бота
$ TG_BOT_TOKEN="1613441681:example"
$ curl -F "url=${PUBLIC_URL}/webhook/" -F "secret_token=webhook_token" https://api.telegram.org/bot${TG_BOT_TOKEN}/setWebhook
{"ok":true,"result":true,"description":"Webhook was set"}
```

### Теперь можно запуcтить бота на локальном сервере django:
`./manage.py runserver`

Если все настройки выполнены правильно и без ошибок, то ваш бот будет отвечать вам вашими же сообщениями

### Готовый пример бота можно скачать здесь:
[Пример эхо-бота](https://github.com/Sergryap/django-bot-project)





