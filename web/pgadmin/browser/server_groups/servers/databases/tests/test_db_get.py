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

from regression.python_test_utils import test_utils as utils


class TestDatabaseGet:
    @pytest.mark.usefixtures('require_database_connection')
    def test_database_get(self, context_of_tests):
        """
        When sending get request to database endpoint
        it returns 200 status
        """

        url = '/browser/database/obj/'
        http_client = context_of_tests['test_client']
        server_id = context_of_tests['server_information']['server_id']
        db_id = context_of_tests['server_information']['db_id']

        response = http_client.get(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' +
            str(db_id), follow_redirects=True)

        response.status_code | should.equal(200)
