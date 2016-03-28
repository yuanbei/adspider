from frontera.settings.default_settings import MIDDLEWARES

SPIDER_PARTITION_ID = 0
MAX_NEXT_REQUESTS = 512
MAX_REQUESTS = 100
DELAY_ON_EMPTY = 5.0

MIDDLEWARES.extend([
    'frontera.contrib.middlewares.domain.DomainMiddleware',
    'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
])

# --------------------------------------------------------
# Crawl frontier backend
# --------------------------------------------------------
BACKEND = 'frontera.contrib.backends.remote.messagebus.MessageBusBackend'

# --------------------------------------------------------
# Logging
# --------------------------------------------------------
LOGGING_ENABLED = True
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = False
LOGGING_BACKEND_ENABLED = False
LOGGING_DEBUGGING_ENABLED = False
