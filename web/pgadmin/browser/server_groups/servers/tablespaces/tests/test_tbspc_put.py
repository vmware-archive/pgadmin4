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

import pytest
from grappa import should

from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as tablespace_utils


class TestTableSpaceUpdate:
    def test_tablespace_put(self, request, context_of_tests):
        """
        When the Tablespace PUT request is send to the backend
        it returns 200 status
        """
        self.server = context_of_tests['server']
        server_id = context_of_tests['server_information']['server_id']
        http_client = context_of_tests['test_client']
        url = '/browser/tablespace/obj/'

        if not self.server['tablespace_path'] \
           or self.server['tablespace_path'] is None:
            message = 'Tablespace delete test case. Tablespace path' \
                      ' not configured for server: %s' % self.server['name']
            pytest.skip(message)

        request.addfinalizer(self.tearDown)

        self.tablespace_name = 'tablespace_delete_%s' % str(uuid.uuid4())[1:8]
        tablespace_id = tablespace_utils.create_tablespace(
            self.server,
            self.tablespace_name)

        tablespace_exists = tablespace_utils.tablespace_exists(
            self.server,
            self.tablespace_name)
        if not tablespace_exists:
            raise Exception('No tablespace(s) to update!!!')

        data = {
            'description': 'This is test description.',
            'table_space_id': tablespace_id
        }
        response = http_client.put(
            url + str(utils.SERVER_GROUP) +
            '/' + str(server_id) + '/' + str(tablespace_id),
            data=json.dumps(data),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
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
