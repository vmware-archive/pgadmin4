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

from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as roles_utils


class TestRoleDelete:
    def test_role_delete(self, request, context_of_tests):
        """
        When the role DELETE request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/role/obj/'
        http_client = context_of_tests['test_client']

        self.server = context_of_tests['server']
        server_id = context_of_tests['server_information']['server_id']
        self.role_name = 'role_delete_%s' % str(uuid.uuid4())[1:8]
        role_id = roles_utils.create_role(self.server, self.role_name)

        response = http_client.delete(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' + str(role_id),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Role dropped')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        roles_utils.delete_role(connection, self.role_name)
