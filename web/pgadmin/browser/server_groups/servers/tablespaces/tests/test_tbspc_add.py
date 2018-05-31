##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import print_function

import json

import pytest
from grappa import should

from pgadmin.utils import server_utils as server_utils
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression.python_test_utils import test_utils as utils
from . import utils as tablespace_utils


class TestTableSpaceAdd:
    def test_add_tablespace(self, request, context_of_tests):
        """
        When a request is sent to add a new tablespace is valid
        It return success
        """
        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']

        self.tablespace_name = ''
        if not self.server['tablespace_path'] \
           or self.server['tablespace_path'] is None:
            message = 'Tablespace add test case. Tablespace path' \
                      ' not configured for server: %s' % self.server['name']
            pytest.skip(message)

        url = '/browser/tablespace/obj/'
        http_client = context_of_tests['test_client']

        server_id = context_of_tests['server_information']['server_id']
        server_response = server_utils.client_connect_server(
            http_client,
            server_id,
            self.server['db_password'])
        if not server_response['data']['connected']:
            raise Exception('Unable to connect server to get tablespace.')

        db_owner = server_response['data']['user']['name']
        table_space_path = self.server['tablespace_path']
        data = tablespace_utils.get_tablespace_data(
            table_space_path, db_owner)
        self.tablespace_name = data['name']
        response = http_client.post(
            url + str(utils.SERVER_GROUP) + '/' + str(server_id) + '/',
            data=json.dumps(data),
            content_type='html/json'
        )

        response.status_code | should.be.equal(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'tablespace',
            'pgadmin.node.tablespace',
            False,
            'icon-tablespace',
            self.tablespace_name
        )

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        tablespace_utils.delete_tablespace(connection, self.tablespace_name)
