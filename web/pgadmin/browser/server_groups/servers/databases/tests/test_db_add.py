##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json

from grappa import should

from pgadmin.utils import server_utils as server_utils
from regression.python_test_utils import test_utils as utils
from . import utils as database_utils


class TestDatabaseAdd:

    def test_database_add(self, request, context_of_tests):
        """
        When sending post request to database endpoint
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

        db_owner = server_response['data']['user']['name']
        data = database_utils.get_db_data(db_owner)
        data['template'] = 'template0'
        self.db_name = data['name']

        response = http_client.post(
            url + str(utils.SERVER_GROUP) + "/" +
            str(server_id) + "/",
            data=json.dumps(data),
            content_type='html/json')

        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        db_id = response_data['node']['_id']
        db_dict = {
            "server_id": server_id,
            "db_id": db_id,
            "db_name": 'baa'
        }

        utils.write_node_info("did", db_dict)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'])
        utils.drop_database(connection, self.db_name)
