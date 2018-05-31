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
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression.python_test_utils import test_utils as utils
from . import utils as roles_utils


class TestRoleAdd:
    def test_add_new_role(self, request, context_of_tests):
        """
        When a request is sent to add a new Role is valid
        It return success
        """
        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']
        http_client = context_of_tests['test_client']
        url = '/browser/role/obj/'
        server_id = context_of_tests['server_information']['server_id']
        server_response = server_utils.client_connect_server(
            http_client,
            server_id,
            self.server['db_password'])
        if not server_response['data']['connected']:
            raise Exception('Server not found to add the role.')

        data = roles_utils.get_role_data(self.server['db_password'])
        self.role_name = data['rolname']
        response = http_client.post(
            url + str(utils.SERVER_GROUP) + '/' + str(server_id) + '/',
            data=json.dumps(data),
            content_type='html/json'
        )
        response.status_code | should.be.equal(200)

        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'role',
            'pgadmin.node.role',
            False,
            'icon-group',
            self.role_name
        )

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        roles_utils.delete_role(connection, self.role_name)
