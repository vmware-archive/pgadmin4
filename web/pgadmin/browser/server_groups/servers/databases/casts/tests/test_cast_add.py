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

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.tests_helper import ClientTestBaseClass
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as cast_utils


@pytest.mark.skip_databases(['gpdb'])
class TestCastsAdd(ClientTestBaseClass):
    def test_check_cast_node(self):
        """
        When creation request is sent to the backend
        it returns 200 status """
        url = '/browser/cast/obj/'
        self.server_data = parent_node_dict["database"][-1]
        self.server_id = self.server_data["server_id"]
        self.db_id = self.server_data['db_id']
        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        self.data = cast_utils.get_cast_data()
        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(
                self.db_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')
        response.status_code | should.be.equal.to(200)

        json_response = self.response_to_json(response)
        self.assert_node_json(json_response,
                              'cast',
                              'pgadmin.node.cast',
                              False,
                              'icon-cast',
                              'money->bigint')

    def tearDown(self):
        connection = utils.get_db_connection(self.server_data['db_name'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        cast_utils.drop_cast(connection, self.data["srctyp"],
                             self.data["trgtyp"])
        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
