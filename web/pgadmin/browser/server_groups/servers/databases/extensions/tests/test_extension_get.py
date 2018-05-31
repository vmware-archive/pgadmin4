##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import print_function

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.tests_helper import ClientTestBaseClass
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as extension_utils


@pytest.mark.skip_databases(['gpdb'])
class TestExtensionsGet(ClientTestBaseClass):
    def test_get_extension(self):
        """
        When get request is sent to the backend
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
        response = self.tester.get(
            url + str(utils.SERVER_GROUP) + '/' + str(
                self.server_id) + '/' +
            str(self.db_id) + '/' + str(self.extension_id),
            content_type='html/json')
        response.status_code | should.be.equal.to(200)
        json_response = self.response_to_json(response)

        json_response | should.have.key('eid')
        json_response | should.have.key('owner') > \
            should.be.equal.to(self.server['username'])
        json_response | should.have.key('name') > should.be.equal.to('cube')
        json_response | should.have.key('schema') > \
            should.be.equal.to(self.schema_name)
        json_response | should.have.key('relocatable') > should.be.true
        json_response | should.have.key('version')
        json_response | should.have.key('comment')

    def tearDown(self):
        """This function disconnect the test database and drop added
         extension."""
        extension_utils.drop_extension(self.server, self.db_name,
                                       self.extension_name)
        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
