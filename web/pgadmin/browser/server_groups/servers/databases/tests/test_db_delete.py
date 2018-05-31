##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import uuid

from grappa import should

from pgadmin.utils import server_utils as server_utils
from regression.python_test_utils import test_utils as utils


class TestDatabaseDelete:

    def test_database_delete(self, request, context_of_tests):
        """
        When sending delete request to database endpoint
        it returns 200 status
        """

        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']
        http_client = context_of_tests['test_client']
        url = '/browser/database/obj/'
        server_id = context_of_tests['server_information']['server_id']
        server_response = server_utils.client_connect_server(
            http_client,
            server_id,
            self.server['db_password'])
        if not server_response['data']['connected']:
            raise Exception('Server not found.')

        self.db_name = "db_%s" % str(uuid.uuid4())[1:8],
        db_id = utils.create_database(self.server, self.db_name)
        db_dict = {
            "server_id": server_id,
            "db_id": db_id,
            "db_name": self.db_name
        }
        utils.write_node_info("did", db_dict)

        response = http_client.delete(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' +
            str(db_id),
            follow_redirects=True)

        response.status_code | should.equal(200)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        utils.drop_database(connection, self.db_name)
