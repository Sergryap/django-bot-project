from typing import Literal, Any

from pydantic import BaseSettings, BaseModel, PostgresDsn, AnyHttpUrl, Field, validator


LogLevel = Literal[
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
]


class TelegramSettings(BaseModel):
    WEBHOOK_TOKEN: str = ''
    BOT_TOKEN: str


def parse_comma_separated(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    return [item.strip() for item in value.split(",")]


class DjangoSettings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = Field(
        default=False,
        description='Disabled by default to protect admin from credentials leak on production environment '
                    'when env param get wrong value. That happends because of param name typos '
                    'and another common configuration mistakes.',
    )
    ALLOWED_HOSTS: list[str] = ['127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS: list[str] = Field(
        default=[],
        description='Trusted origins for CSRF checks.',
    )

    STATIC_URL: str = 'static/'
    MEDIA_URL: str = 'media/'

    parse_comma_separated_values = validator('ALLOWED_HOSTS', 'CSRF_TRUSTED_ORIGINS', pre=True, allow_reuse=True)(
        parse_comma_separated,
    )


class RollbarSettings(BaseSettings):
    BACKEND_TOKEN: str
    ENVIRONMENT: str


class EnvSettings(BaseSettings):
    DJ: DjangoSettings

    POSTGRES_DSN: PostgresDsn | None = None

    TEMPLATES_ARE_CACHED: bool = False

    ENABLE_MEDIA_FILES_SERVING: bool = Field(
        default=False,
        description='Enables serving of media files with Django app server. This feature simplifies development '
                    'process and not suitable for production environment.',
    )

    ENABLE_DEBUG_TOOLBAR: bool = Field(
        default=False,
        description='Disabled by default to protect admin from credentials leak on production environment '
                    'when ENABLE_DEBUG_TOOLBAR env params get wrong value. That happends because of '
                    'param name typos and another common configuration mistakes.',
    )

    WEBAPP_ROOT_URL: AnyHttpUrl = Field(
        description='Web application URL to access from frontend. E.g. http://127.0.0.1:8000/.',
    )

    ROLLBAR: RollbarSettings | None

    TG_BOT_LOGGING_LEVEL: LogLevel = Field(to_lower=True, strip_whitespace=True, default='WARNING')
    DJANGO_TG_BOT_FRAMEWORK_LOGGING_LEVEL: LogLevel = Field(to_lower=True, strip_whitespace=True, default='WARNING')
    DJANGO_TG_BOT_FRAMEWORK_MOCK_MESSAGES_ENABLED: bool = Field(
        default=False,
        description='Disabled by default to protect admin from incorrect bot behaviour on production environment '
                    'when env param get wrong value. That happends because of '
                    'param name typos and another common configuration mistakes.',
    )

    TG: TelegramSettings

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
        case_sensitive = True
        validate_all = True
