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
import uuid

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from regression.python_test_utils import test_utils as utils
from . import utils as fdw_utils


@pytest.mark.skip_databases(['gpdb'])
class TestForeignDataWrapperPut:
    def test_foreign_data_wrapper_put(self, request, context_of_tests):
        """
        When sending a HTTP request to put a foreign data wrapper update
        It returns 200 status
        """

        request.addfinalizer(self.tearDown)

        url = '/browser/foreign_data_wrapper/obj/'

        schema_data = context_of_tests['server_information']
        self.server = context_of_tests['server']
        self.server_id = schema_data['server_id']
        self.db_id = schema_data['db_id']
        self.db_name = schema_data["db_name"]
        self.fdw_name = "fdw_put_{0}".format(str(uuid.uuid4())[1:8])
        fdw_id = fdw_utils.create_fdw(self.server, self.db_name,
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

        fdw_utils.verify_fdw(self.server, self.db_name, self.fdw_name) | \
            should.not_be.none

        data = {
            "description": "This is FDW update comment",
            "id": fdw_id
        }

        put_response = self.tester.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' + str(fdw_id),
            data=json.dumps(data),
            follow_redirects=True)

        put_response.status_code | should.be.equal.to(200)

    def tearDown(self):
        fdw_utils.delete_fdw(self.server, self.db_name, self.fdw_name)
        database_utils.client_disconnect_database(
            self.tester,
            self.server_id,
            self.db_id)
