import os

env_name = os.getenv('RUN_ENV', 'prod')

if env_name == 'prod':
    from .prod import *
elif env_name == 'staging':
    from .staging import *
else:
    from .dev import *
