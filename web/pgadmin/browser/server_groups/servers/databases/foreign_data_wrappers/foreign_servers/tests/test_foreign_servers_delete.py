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

from pgadmin.browser.server_groups.servers.databases.extensions.tests import \
    utils as extension_utils
from pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers. \
    tests import utils as fdw_utils
from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from regression.python_test_utils import test_utils as utils
from . import utils as fsrv_utils


@pytest.mark.skip_databases(['gpdb'])
class TestForeignServerDelete:
    def test_foreign_server_delete(self, request, context_of_tests):
        """
        When sending a HTTP request to
        delete foreign server under database node
        It returns 200 status
        """

        request.addfinalizer(self.tearDown)

        url = '/browser/foreign_server/obj/'

        schema_data = context_of_tests['server_information']
        self.server = context_of_tests['server']
        self.server_id = schema_data['server_id']
        self.db_id = schema_data['db_id']
        self.db_name = schema_data["db_name"]
        self.schema_name = schema_data['schema_name']
        self.extension_name = 'cube'
        self.fdw_name = "test_fdw_%s" % (str(uuid.uuid4())[1:8])
        self.fsrv_name = "test_fsrv_%s" % (str(uuid.uuid4())[1:8])
        extension_utils.create_extension(
            self.server, self.db_name, self.extension_name, self.schema_name)
        self.fdw_id = fdw_utils.create_fdw(self.server, self.db_name,
                                           self.fdw_name)
        fsrv_id = fsrv_utils.create_fsrv(self.server, self.db_name,
                                         self.fsrv_name, self.fdw_name)

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

        # fdw_utils.verify_fdw(self.server, self.db_name, self.fdw_name) | \
        #     should.not_be.none

        fdw_utils.verify_fdw(self.server, self.db_name, self.fdw_name) | \
            should.not_be.equal.to(None, msg='Could not find FDW.')

        fsrv_utils.verify_fsrv(self.server, self.db_name, self.fsrv_name) | \
            should.not_be.equal.to(None, msg='Could not find FSRV.')

        delete_response = self.tester.delete(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.fdw_id) + '/' +
            str(fsrv_id),
            follow_redirects=True)

        delete_response.status_code | should.be.equal.to(200)

    def tearDown(self):
        extension_utils.drop_extension(self.server, self.db_name,
                                       self.extension_name)
        database_utils.client_disconnect_database(self.tester,
                                                  self.server_id,
                                                  self.db_id)
