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

from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from regression.python_test_utils import test_utils as utils
from . import utils as fdw_utils


@pytest.mark.skip_databases(['gpdb'])
class TestForeignDataWrapperAdd:
    def test_foreign_data_wrapper_add(self, request, context_of_tests):
        """
        When sending a valid HTTP request to add a foreign data wrapper
        It returns 200 status
        """

        request.addfinalizer(self.tearDown)

        url = '/browser/foreign_data_wrapper/obj/'

        schema_data = context_of_tests['server_information']
        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_id = schema_data['server_id']
        self.db_id = schema_data['db_id']
        self.schema_name = schema_data['schema_name']
        self.db_name = schema_data["db_name"]

        db_con = database_utils.client_connect_database(
            self.tester,
            utils.SERVER_GROUP,
            self.server_id,
            self.db_id,
            self.server["db_password"])

        db_con["info"] | should.be.equal.to(
            "Database connected.",
            msg='Could not connect to database.')

        self.data = fdw_utils.get_fdw_data(self.schema_name,
                                           self.server['username'])
        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)

        assert_json_values_from_response(json_response,
                                         'foreign_data_wrapper',
                                         'pgadmin.node.foreign_data_wrapper',
                                         True,
                                         'icon-foreign_data_wrapper',
                                         self.data['name'])

    def tearDown(self):
        if hasattr(self, 'data'):
            fdw_utils.delete_fdw(self.server, self.db_name, self.data["name"])
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
