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
