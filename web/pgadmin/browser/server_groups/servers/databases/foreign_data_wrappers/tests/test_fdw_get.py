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
from regression.python_test_utils import test_utils as utils
from . import utils as fdw_utils


@pytest.mark.skip_databases(['gpdb'])
class TestForeignDataWrapperGet:
    def test_foreign_data_wrapper_get(self, request, context_of_tests):
        """
        When sending a valid HTTP request to add a foreign data wrapper
        It returns 200 status
        """

        request.addfinalizer(self.tearDown)

        url = '/browser/foreign_data_wrapper/obj/'

        schema_data = context_of_tests['server_information']
        self.server = context_of_tests['server']
        self.server_id = schema_data['server_id']
        self.db_id = schema_data['db_id']
        self.db_name = schema_data["db_name"]
        self.schema_name = schema_data['schema_name']
        self.fdw_name = "fdw_{0}".format(str(uuid.uuid4())[1:8])
        self.fdw_id = fdw_utils.create_fdw(self.server,
                                           self.db_name,
                                           self.fdw_name)

        self.tester = context_of_tests['test_client']

        db_con = database_utils.client_connect_database(
            self.tester,
            utils.SERVER_GROUP,
            self.server_id,
            self.db_id,
            self.server['db_password'])

        db_con["info"] | should.be.equal.to(
            "Database connected.",
            msg='Could not connect to database.')

        response = self.tester.get(
            url + str(utils.SERVER_GROUP) + '/' + str(
                self.server_id) + '/' +
            str(self.db_id) + '/' + str(self.fdw_id),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)

    def tearDown(self):
        fdw_utils.delete_fdw(self.server, self.db_name, self.fdw_name)

        database_utils.client_disconnect_database(self.tester,
                                                  self.server_id,
                                                  self.db_id)
