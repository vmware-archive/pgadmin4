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


class TestRoleGet:
    def test_role_get(self, request, context_of_tests):
        """
        When the role GET request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/role/obj/'
        http_client = context_of_tests['test_client']

        self.server = context_of_tests['server']
        server_id = context_of_tests['server_information']['server_id']

        self.role_name = 'role_get_%s' % str(uuid.uuid4())[1:8]
        role_id = roles_utils.create_role(self.server, self.role_name)

        response = http_client.get(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' + str(role_id),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('oid')
        json_response | should.have.key('oid-2')
        json_response | should.have.key('rolpassword') > \
            should.be.equal.to('')
        json_response | should.have.key('rolcreatedb') > \
            should.be.false
        json_response | should.have.key('rolsuper') > \
            should.be.false
        json_response | should.have.key('rolcreaterole') > \
            should.be.false
        json_response | should.have.key('rolcatupdate') > \
            should.be.false
        json_response | should.have.key('rolname') > \
            should.be.equal.to(self.role_name)
        json_response | should.have.key('rolvaliduntil') > \
            should.be.none
        json_response | should.have.key('rolcanlogin') > \
            should.be.true
        json_response | should.have.key('description') > \
            should.be.none
        json_response | should.have.key('rolinherit') > \
            should.be.true
        json_response | should.have.key('rolconfig') > \
            should.be.none
        json_response | should.have.key('rolmembership') > \
            should.be.equal.to([])

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        roles_utils.delete_role(connection, self.role_name)
