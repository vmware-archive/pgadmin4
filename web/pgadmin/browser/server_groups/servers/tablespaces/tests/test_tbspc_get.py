##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import uuid

import pytest
from grappa import should

from pgadmin.utils import server_utils as server_utils
from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as tablespace_utils


class TestTablespaceGet:
    def test_tablespace_get(self, request, context_of_tests):
        """
        When the tablespace GET request is send to the backend
        it returns 200 status
        """
        self.server = context_of_tests['server']

        if not self.server['tablespace_path'] \
           or self.server['tablespace_path'] is None:
            message = 'Tablespace get test case. Tablespace path' \
                      ' not configured for server: %s' % self.server['name']
            pytest.skip(message)

        request.addfinalizer(self.tearDown)

        url = '/browser/tablespace/obj/'
        http_client = context_of_tests['test_client']

        self.tablespace_name = 'tablespace_delete_%s' % str(uuid.uuid4())[1:8]
        tablespace_id = tablespace_utils.create_tablespace(
            self.server,
            self.tablespace_name)

        server_id = context_of_tests['server_information']['server_id']

        server_response = server_utils.client_connect_server(
            http_client,
            server_id,
            self.server['db_password'])
        if not server_response['data']['connected']:
            raise Exception('Unable to connect server to get tablespace.')

        tablespace_exists = tablespace_utils.tablespace_exists(
            self.server,
            self.tablespace_name)
        if not tablespace_exists:
            raise Exception('No tablespace(s) to update!!!')

        response = http_client.get(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' + str(tablespace_id),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('spcacl') > \
            should.be.equal.to([])
        json_response | should.have.key('name') > \
            should.be.equal.to(self.tablespace_name)
        json_response | should.have.key('spcoptions') > \
            should.be.none
        json_response | should.have.key('oid')
        json_response | should.have.key('spclocation') > \
            should.be.equal.to(self.server['tablespace_path'].rstrip('/\\'))
        json_response | should.have.key('acl') > \
            should.be.none
        json_response | should.have.key('spcuser') > \
            should.be.equal.to(self.server['username'])
        json_response | should.have.key('seclabels') > \
            should.be.none
        json_response | should.have.key('description') > \
            should.be.none

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        tablespace_utils.delete_tablespace(connection, self.tablespace_name)
