##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import print_function

import uuid

import pytest
from grappa import should

from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as tablespace_utils


class TestTableSpaceDelete:
    def test_tablespace_delete(self, request, context_of_tests):
        """
        When the tablespace DELETE request is send to the backend
        it returns 200 status
        """
        url = '/browser/tablespace/obj/'
        http_client = context_of_tests['test_client']

        self.server = context_of_tests['server']
        if not self.server['tablespace_path'] \
           or self.server['tablespace_path'] is None:
            message = 'Tablespace delete test case. Tablespace path' \
                      ' not configured for server: %s' % self.server['name']
            # Skip the test case if tablespace_path not found.
            pytest.skip(message)

        request.addfinalizer(self.tearDown)

        self.tablespace_name = 'tablespace_delete_%s' % str(uuid.uuid4())[1:8]
        server_id = context_of_tests['server_information']['server_id']
        tablespace_id = tablespace_utils.create_tablespace(
            self.server, self.tablespace_name)

        tablespace_exists = tablespace_utils.tablespace_exists(
            self.server,
            self.tablespace_name)
        if not tablespace_exists:
            raise Exception('No tablespace(s) to delete!!!')

        response = http_client.delete(
            url + str(utils.SERVER_GROUP) +
            '/' + str(server_id) + '/' + str(tablespace_id),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Tablespace dropped')
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
        tablespace_utils.delete_tablespace(connection, self.tablespace_name)
