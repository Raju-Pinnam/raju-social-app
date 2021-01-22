from .base import *

if config('ENV') == 'LOCAL':
    from .local import *
elif config('ENV') == 'PROD':
    from .prod import *
