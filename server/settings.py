try:
    from server.conf.local import *
except ImportError:
    from server.conf.default import *