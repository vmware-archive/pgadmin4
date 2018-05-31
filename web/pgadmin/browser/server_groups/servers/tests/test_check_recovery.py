import os

import pytest
from grappa import should

from regression.python_test_utils import test_utils


class TestCheckRecovery:
    def test_check_recovery(self, context_of_tests):
        """
        When loading the check_recovery.sql
        it loads false for inrecovery and wal_paused
        """

        server = context_of_tests['server']

        cursor = test_utils.get_db_connection(
            server['db'],
            server['username'],
            server['db_password'],
            server['host'],
            server['port'],
            server['sslmode']).cursor()

        if cursor is None or cursor.connection is None:
            pytest.skip('Provided server does not have a cursor')

        server_version = cursor.connection.server_version
        if server_version >= 100000:
            version = '10_plus'
        elif server_version >= 90000:
            version = '9.0_plus'
        else:
            version = 'default'

        template_file = os.path.join(
            os.path.dirname(__file__), "../templates/connect/sql", version,
            "check_recovery.sql"
        )

        cursor.execute(open(template_file, 'r').read())
        fetch_result = cursor.fetchall()

        first_row = {}
        for index, description in enumerate(cursor.description):
            first_row[description.name] = fetch_result[0][index]

        first_row['inrecovery'] | should.be.false
        first_row['isreplaypaused'] | should.be.false
