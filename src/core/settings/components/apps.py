# fmt: off
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",

    "apps.campaigns.apps.CampaignsConfig",
    "apps.strategies.apps.StrategiesConfig",
    "models.apps.ModelsConfig",
]
# fmt: on
