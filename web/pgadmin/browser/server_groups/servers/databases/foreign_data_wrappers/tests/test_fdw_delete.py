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

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as fdw_utils


@pytest.mark.skip_databases(['gpdb'])
class TestForeignDataWrapperDelete:
    def test_foreign_data_wrapper_delete(self, request, context_of_tests):
        """
        When sending a HTTP request to delete a foreign data wrapper
        It returns 200 status
        """

        request.addfinalizer(self.tearDown)

        self.server_information = context_of_tests['server_information']
        self.tester = context_of_tests['test_client']
        server = context_of_tests['server']

        self.server_id = self.server_information["server_id"]

        url = '/browser/foreign_data_wrapper/obj/'

        schema_data = context_of_tests['server_information']
        self.server_id = schema_data['server_id']
        self.db_id = schema_data['db_id']
        self.db_name = schema_data["db_name"]
        self.schema_name = schema_data['schema_name']
        self.fdw_name = "fdw_{0}".format(str(uuid.uuid4())[1:8])
        self.fdw_id = fdw_utils.create_fdw(server, self.db_name,
                                           self.fdw_name)

        db_con = database_utils.client_connect_database(
            self.tester,
            utils.SERVER_GROUP,
            self.server_id,
            self.db_id,
            server["db_password"])

        db_con["info"] | should.be.equal.to(
            "Database connected.",
            msg='Could not connect to database.')

        fdw_utils.verify_fdw(server, self.db_name, self.fdw_name) | \
            should.not_be.none

        response = self.tester.delete(url +
                                      str(utils.SERVER_GROUP) +
                                      '/' + str(self.server_id) + '/' +
                                      str(self.db_id) +
                                      '/' + str(self.fdw_id),
                                      follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)

        json_response | should.have.key('info') > should.be.equal.to(
            'Foreign Data Wrapper dropped')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)

    def tearDown(self):
        database_utils.client_disconnect_database(
            self.tester,
            self.server_information['server_id'],
            self.db_id)
