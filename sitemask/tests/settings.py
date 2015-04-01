SECRET_KEY = 'Not so secret.'

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS = ('sitemask',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
