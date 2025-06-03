from pathlib import Path

import environ
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

envpath = BASE_DIR.parent / ".env"

if envpath.exists():
    env.read_env(envpath)

DEBUG = env.bool("DEBUG", default=False)

ROOT_URLCONF = "core.urls"

SECRET_KEY = env("SECRET_KEY")

WSGI_APPLICATION = "core.wsgi.application"

include("components/*.py")
