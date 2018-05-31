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
from . import utils as extension_utils


@pytest.mark.skip_databases(['gpdb'])
class TestExtensionsPut(ClientTestBaseClass):
    def test_extensions_put(self):
        """
        When PUT request is sent to the backend
        it returns 200 status"""
        url = '/browser/extension/obj/'
        self.schema_data = parent_node_dict['schema'][-1]
        self.server_id = self.schema_data['server_id']
        self.db_id = self.schema_data['db_id']
        self.schema_name = self.schema_data['schema_name']
        self.extension_name = "cube"
        self.db_name = parent_node_dict["database"][-1]["db_name"]
        self.extension_id = extension_utils.create_extension(
            self.server, self.db_name, self.extension_name, self.schema_name)

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")
        response = extension_utils.verify_extension(self.server, self.db_name,
                                                    self.extension_name)
        if not response:
            raise Exception("Could not find extension.")
        data = {
            "schema": "public",
            "id": self.extension_id
        }
        response = self.tester.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(
                self.db_id) +
            '/' + str(self.extension_id),
            data=json.dumps(data),
            follow_redirects=True)
        response.status_code | should.be.equal.to(200)

        json_response = self.response_to_json(response)
        self.assert_node_json(json_response,
                              'extension',
                              'pgadmin.node.extension',
                              False,
                              'icon-extension',
                              'cube')

    def tearDown(self):
        """This function disconnect the test database and drop added
        extension."""
        extension_utils.drop_extension(self.server, self.db_name,
                                       self.extension_name)
        database_utils.disconnect_database(self, self.server_id, self.db_id)
