##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import pytest
from grappa import should

from regression.python_test_utils import test_utils


class TestSSLConnection:
    def test_ssl_connection(self, context_of_tests):
        """
        It verifies SSL connection
        """
        server = context_of_tests['server']

        supported_modes = ['require', 'verify-ca', 'verify-full']
        if server['sslmode'] not in supported_modes:
            pytest.skip(
                'Cannot run SSL connection check test '
                'with \'{0}\' sslmode'.format(server['sslmode'])
            )

        with test_utils.Database(server) as (
            connection, database_name
        ):
            cursor = connection.cursor()
            cursor.execute("CREATE EXTENSION sslinfo")
            connection.commit()
            cursor.execute("SELECT ssl_is_used()")
            cursor.fetchone()[0] | should.equal('True')
