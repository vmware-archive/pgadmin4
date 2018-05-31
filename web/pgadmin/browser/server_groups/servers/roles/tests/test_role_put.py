##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

from grappa import should

from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression.python_test_utils import test_utils as utils
from . import utils as roles_utils


class TestRolePut:
    def test_role_put(self, request, context_of_tests):
        """
        When the Role PUT request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']
        http_client = context_of_tests['test_client']
        url = '/browser/role/obj/'

        server_id = context_of_tests['server_information']['server_id']
        self.role_name = 'role_put_%s' % str(uuid.uuid4())[1:8]
        role_id = roles_utils.create_role(self.server, self.role_name)

        is_role_verified = roles_utils.verify_role(self.server, self.role_name)
        if len(is_role_verified) == 0:
            raise Exception('No roles(s) to update!!!')

        data = {
            'description': 'This is the test description for cast',
            'lrid': role_id
        }
        response = http_client.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' + str(role_id),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'role',
            'pgadmin.node.role',
            False,
            'icon-role',
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
