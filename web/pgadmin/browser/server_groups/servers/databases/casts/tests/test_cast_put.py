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
class TestCastsPut(ClientTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup):
        self.default_db = self.server["db"]
        self.database_info = parent_node_dict['database'][-1]
        self.db_name = self.database_info['db_name']
        self.server["db"] = self.db_name
        self.source_type = 'character'
        self.target_type = 'cidr'
        self.cast_id = cast_utils.create_cast(self.server, self.source_type,
                                              self.target_type)

    def test_put(self):
        """When a cast exits
         When updating the cast,
         It gets updates the cast in the database
          And return 200 status"""
        url = '/browser/cast/obj/'
        self.server_id = self.database_info["server_id"]
        self.db_id = self.database_info['db_id']
        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'])
        response = cast_utils.verify_cast(connection, self.source_type,
                                          self.target_type)
        if len(response) == 0:
            raise Exception("Could not find cast.")
        data = {
            "description": "This is cast update comment",
            "id": self.cast_id
        }
        put_response = self.tester.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(
                self.db_id) +
            '/' + str(self.cast_id),
            data=json.dumps(data),
            follow_redirects=True)
        put_response.status_code | should.be.equal.to(200)

        json_response = self.response_to_json(put_response)
        self.assert_node_json(json_response,
                              'cast',
                              'pgadmin.node.cast',
                              False,
                              'icon-cast',
                              'character->cidr')

    def tearDown(self):
        """This function disconnect the test database and drop added cast."""
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'])
        cast_utils.drop_cast(connection, self.source_type,
                             self.target_type)
        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
        self.server['db'] = self.default_db
