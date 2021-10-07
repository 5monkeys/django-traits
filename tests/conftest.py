from django.conf import settings


def pytest_configure() -> None:
    settings.configure(
        INSTALLED_APPS=["tests.app"],
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
    )
