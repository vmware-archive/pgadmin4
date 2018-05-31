import pytest
import six

from pgadmin.utils.route import TestsGeneratorRegistry

from enum import Enum


class PostgresVersion(Enum):
    v10 = 100000
    v96 = 90600
    v95 = 90500
    v94 = 90400
    v93 = 90300
    v92 = 90200
    v91 = 90100
    v90 = 90000
    v83 = 80323

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        if type(other) == int:
            return self.value > other
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        if type(other) == int:
            return self.value < other
        return NotImplemented


@six.add_metaclass(TestsGeneratorRegistry)
class BaseTestGenerator(object):
    @pytest.fixture(autouse=True)
    def check_if_test_should_be_skipped(self, request, get_server_type,
                                        get_server_version):
        self.__skip_if_database(get_server_type, request)
        self.__skip_if_postgres_version(get_server_version, request)

    @pytest.fixture(autouse=True)
    def the_real_setup(self, context_of_tests):
        if not hasattr(self, 'setup_not_needed'):
            self.server_information = context_of_tests['server_information']
            self.tester = context_of_tests['test_client']
            self.server = context_of_tests['server']

            self.server_id = self.server_information["server_id"]

        yield context_of_tests
        self.tearDown()

    def tearDown(self):
        pass

    def _expand_test_object(self, kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __skip_if_database(self, get_server_type, request):
        if request.node.get_marker('skip_databases'):
            if get_server_type in \
               request.node.get_marker('skip_databases').args[0]:
                pytest.skip('cannot run in: %s' %
                            get_server_type)

    def __skip_if_postgres_version(self, get_server_version, request):
        if request.node.get_marker('skip_if_postgres_version'):
            versions = \
                request.node.get_marker('skip_if_postgres_version').args[0]
            skip_message = \
                request.node.get_marker('skip_if_postgres_version').args[1]
            if versions['below_version'] > get_server_version:
                pytest.skip(skip_message)
