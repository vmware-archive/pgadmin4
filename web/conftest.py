##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import atexit
import logging
import os
import signal
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)
file_name = os.path.basename(__file__)

if sys.version_info < (2, 7):
    pass
else:
    pass

if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins

# Ensure the global server mode is set.
builtins.SERVER_MODE = None

logger = logging.getLogger(__name__)
file_name = os.path.basename(__file__)

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

root = os.path.dirname(CURRENT_PATH) + os.path.sep + 'web'

if sys.path[0] != root:
    sys.path.insert(0, root)
    os.chdir(root)

from pgadmin import create_app
import config
if config.SERVER_MODE is True:
    config.SECURITY_RECOVERABLE = True
    config.SECURITY_CHANGEABLE = True
    config.SECURITY_POST_CHANGE_VIEW = 'browser.change_password'

from pgadmin.browser.server_groups.servers.databases.tests.utils import \
    client_connect_database, client_disconnect_database
from pgadmin.utils import server_utils
from regression import test_setup

from regression.feature_utils.app_starter import AppStarter

if config.SERVER_MODE is True:
    config.SECURITY_RECOVERABLE = True
    config.SECURITY_CHANGEABLE = True
    config.SECURITY_POST_CHANGE_VIEW = 'browser.change_password'

from regression.feature_utils.app_starter import AppStarter

# Delete SQLite db file if exists
if os.path.isfile(config.TEST_SQLITE_PATH):
    os.remove(config.TEST_SQLITE_PATH)

os.environ["PGADMIN_TESTING_MODE"] = "1"

# Disable upgrade checks - no need during testing, and it'll cause an error
# if there's no network connection when it runs.
config.UPGRADE_CHECK_ENABLED = False

pgadmin_credentials = test_setup.config_data

# Set environment variables for email and password
os.environ['PGADMIN_SETUP_EMAIL'] = ''
os.environ['PGADMIN_SETUP_PASSWORD'] = ''
if pgadmin_credentials:
    if 'pgAdmin4_login_credentials' in pgadmin_credentials:
        if all(item in pgadmin_credentials['pgAdmin4_login_credentials']
               for item in ['login_username', 'login_password']):
            pgadmin_credentials = pgadmin_credentials[
                'pgAdmin4_login_credentials']
            os.environ['PGADMIN_SETUP_EMAIL'] = str(
                pgadmin_credentials['login_username'])
            os.environ['PGADMIN_SETUP_PASSWORD'] = str(
                pgadmin_credentials['login_password'])

# Execute the setup file
exec(open(os.path.join(root, "setup.py")).read())

# Get the config database schema version. We store this in pgadmin.model
# as it turns out that putting it in the config files isn't a great idea
from pgadmin.model import SCHEMA_VERSION

# Delay the import test_utils as it needs updated config.SQLITE_PATH
from regression.python_test_utils import test_utils

config.SETTINGS_SCHEMA_VERSION = SCHEMA_VERSION

# Override some other defaults
from logging import WARNING

config.CONSOLE_LOG_LEVEL = WARNING

# Create the app
app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
app.PGADMIN_KEY = ''
app.config.update({'SESSION_COOKIE_DOMAIN': None})
test_client = app.test_client()
driver = None
app_starter = None
handle_cleanup = None

server_info = test_utils.get_config_data()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def database_server(request):
    server_information = test_utils.create_parent_server_node(server_info[0])
    request.addfinalizer(lambda: test_utils.delete_test_server(test_client))

    yield server_information


@pytest.fixture(scope='session')
def context_of_tests(database_server):
    yield {
        'server_information': database_server,
        'test_client': test_client,
        'server': server_info[0]
    }


@pytest.fixture(scope='session')
def gather_current_database_information(context_of_tests):
    server_id = context_of_tests['server_information']['server_id']
    db_password = context_of_tests['server']['db_password']
    http_client = context_of_tests['test_client']
    server_con = server_utils.client_connect_server(http_client, server_id,
                                                    db_password)
    server_data = None
    if 'data' in server_con:
        server_data = server_con['data']
    yield server_data


@pytest.fixture
def get_server_type(gather_current_database_information):
    server_type = None
    if gather_current_database_information and \
       'type' in gather_current_database_information:
        server_type = gather_current_database_information['type']
    yield server_type


@pytest.fixture
def get_server_version(gather_current_database_information):
    server_version = None
    if gather_current_database_information and \
       'version' in gather_current_database_information:
        server_version = gather_current_database_information['version']
    yield server_version


@pytest.fixture
def require_database_connection(context_of_tests):
    server_data = context_of_tests['server_information']
    server_id = server_data['server_id']
    db_id = server_data['db_id']
    http_client = context_of_tests['test_client']

    db_con = client_connect_database(
        http_client,
        test_utils.SERVER_GROUP,
        server_id,
        db_id,
        server_data['db_password'])
    if not db_con["info"] == "Database connected.":
        raise Exception("Could not connect to database.")

    yield db_con

    client_disconnect_database(http_client,
                               server_id,
                               db_id)


@pytest.fixture(scope='session')
def driver():
    options = Options()
    if test_setup.config_data:
        if 'headless_chrome' in test_setup.config_data:
            if test_setup.config_data['headless_chrome']:
                options.add_argument("--headless")
    options.add_argument("--window-size=1280x1024")
    driver = webdriver.Chrome(chrome_options=options)

    app_starter = AppStarter(driver, config)
    app_starter.start_app()

    handle_cleanup = test_utils.get_cleanup_handler(test_client, app_starter)
    # Register cleanup function to cleanup on exit
    atexit.register(handle_cleanup)

    yield driver


@pytest.fixture(scope='function', autouse=True)
def check_if_test_should_be_skipped(request,
                                    get_server_type,
                                    get_server_version):
    __skip_if_database(get_server_type, request)
    __skip_if_postgres_version(get_server_version, request)
    __skip_if_not_in_server_mode(request)


def __skip_if_database(get_server_type, request):
    if request.node.get_marker('skip_databases'):
        if get_server_type in \
           request.node.get_marker('skip_databases').args[0]:
            pytest.skip('cannot run in: %s' %
                        get_server_type)


def __skip_if_postgres_version(get_server_version, request):
    if request.node.get_marker('skip_if_postgres_version'):
        versions = \
            request.node.get_marker('skip_if_postgres_version').args[0]
        skip_message = \
            request.node.get_marker('skip_if_postgres_version').args[1]
        if versions['below_version'] > get_server_version:
            pytest.skip(skip_message)


def __skip_if_not_in_server_mode(request):
    if request.node.get_marker('skip_if_not_in_server_mode'):
        if not config.SERVER_MODE:
            pytest.skip('The application need to be in server mode')


def pytest_generate_tests(metafunc):
    if not hasattr(metafunc.cls, 'scenarios'):
        return

    list_of_scenario_names = []
    scenario_parameters = []
    for scenario in metafunc.cls.scenarios:
        list_of_scenario_names.append(scenario[0])
        scenario_parameters.append(('', scenario[1]))
    metafunc.parametrize('args,kwargs',
                         scenario_parameters,
                         ids=list_of_scenario_names,
                         scope="class",
                         indirect=False)


def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if item._genid is not None:
        suf = item._genid

    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


def sig_handler(signo, frame):
    global handle_cleanup
    if handle_cleanup:
        # Unset environment variable
        del os.environ["PGADMIN_TESTING_MODE"]

        handle_cleanup()


class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.terminal = sys.stderr
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        """
        This function writes the log in the logger file as well as on console

        :param buf: log message
        :type buf: str
        :return: None
        """

        self.terminal.write(buf)
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


# Set signal handler for cleanup
signal_list = dir(signal)
required_signal_list = ['SIGTERM', 'SIGABRT', 'SIGQUIT', 'SIGINT']
# Get the OS wise supported signals
supported_signal_list = [sig for sig in required_signal_list if
                         sig in signal_list]
for sig in supported_signal_list:
    signal.signal(getattr(signal, sig), sig_handler)

# Set basic logging configuration for log file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename=(root + os.path.sep + 'regression' + os.path.sep +
              "regression.log"),
    filemode='w'
)

# Create logger to write log in the logger file as well as on console
stderr_logger = logging.getLogger('STDERR')
sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
