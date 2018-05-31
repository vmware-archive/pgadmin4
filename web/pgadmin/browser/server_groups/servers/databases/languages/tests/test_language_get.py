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

from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as language_utils


class TestLanguagesAdd:
    def test_language_add(self, request, context_of_tests):
        """
        When the language get request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/language/obj/'

        self.server_data = parent_node_dict['database'][-1]
        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        schema_data = context_of_tests['server_information']
        self.db_name = schema_data["db_name"]
        self.lang_name = "language_%s" % str(uuid.uuid4())[1:8]

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        self.language_id = language_utils.create_language(self.server,
                                                          self.db_name,
                                                          self.lang_name)

        response = self.tester.get("{0}{1}/{2}/{3}/{4}".format(
            url, utils.SERVER_GROUP, self.server_id, self.db_id,
            self.language_id), follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('oid')
        json_response | should.have.key('name') > \
            should.be.equal.to(self.lang_name)
        json_response | should.have.key('trusted') > should.be.equal.true
        json_response | should.have.key('acl') > should.be.none
        json_response | should.have.key('description') > should.be.none

    def tearDown(self):
        language_utils.delete_language(
            self.server, self.db_name, self.lang_name
        )
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
