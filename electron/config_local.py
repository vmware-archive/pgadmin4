from config import *

# Log
CONSOLE_LOG_LEVEL = DEBUG
FILE_LOG_LEVEL = DEBUG

UPGRADE_CHECK_ENABLED = False
DEFAULT_SERVER_PORT = 7894

SERVER_MODE = False
if IS_WIN:
    # Use the short path on windows
    DATA_DIR = os.path.realpath(
        os.path.join(fs_short_path(env('APPDATA')), u"pgAdmin")
    )
else:
    DATA_DIR = os.path.realpath(os.path.expanduser(u'~/.pgadmin/'))

# Use a different config DB for each server mode.
SQLITE_PATH = os.path.join(
    DATA_DIR,
    'pgadmin4-desktop.db'
)

LOG_FILE = os.path.join(DATA_DIR, 'pgadmin4.log')

SESSION_DB_PATH = os.path.join(DATA_DIR, 'sessions')
STORAGE_DIR = os.path.join(DATA_DIR, 'storage')
TEST_SQLITE_PATH = os.path.join(DATA_DIR, 'test_pgadmin4.db')

