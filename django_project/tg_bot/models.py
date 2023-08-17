from django.db import models
from django.utils import timezone
from django_tg_bot_framework.models import (
    BaseStateMachineDump,
    TgUserProfileMixin,
    validate_state_class_locator_friendly_to_user,
)
from contextvars import ContextVar


# Will be initialized with current conversation object by state machine runner before states methods run.
conversation_var: ContextVar['Conversation'] = ContextVar('conversation_var')


class Conversation(BaseStateMachineDump, TgUserProfileMixin):
    state_class_locator = models.CharField(
        'Класс состояния',
        max_length=300,
        blank=True,
        help_text='Тип состояния, в котором сейчас находится диалог с пользователем. '
                  'В поле хранится локатор класса состояния, похожий на строку адреса URL. '
                  'Локатор начинается со слэша <code>/</code> и заканчивается слэшом <code>/</code>, '
                  'содержит только латинские символы a-z, цифры, знаки тире, подчёркивания и слэша <code>/</code>. '
                  'Строго нижний регистр букв.',
        validators=[validate_state_class_locator_friendly_to_user],
    )

    tg_chat_id = models.CharField(
        'Id чата в Tg',
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Id чата в Tg, где пользователь общается с ботом.',
    )
    started_at = models.DateTimeField(
        "когда начат",
        db_index=True,
        default=timezone.now,
        help_text="Диалог начинается, когда пользователь присылает боту своё первое сообщение в Tg.",
    )

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        constraints = [
            *BaseStateMachineDump._meta.constraints,
            *TgUserProfileMixin._meta.constraints,
        ]
