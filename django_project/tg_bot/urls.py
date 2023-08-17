from functools import partial

from django.urls import path
from django.conf import settings
from django_tg_bot_framework.views import process_webhook_call

from .models import conversation_var
from .states import router
from .state_machine_runners import process_tg_update


app_name = 'tg_bot'

urlpatterns = [
    path(
        '',
        process_webhook_call,
        kwargs={
            'webhook_token': settings.ENV.TG.WEBHOOK_TOKEN,
            'process_update': partial(process_tg_update, router=router, conversation_var=conversation_var),
        },
        name='process_webhook_call',
    ),
]
