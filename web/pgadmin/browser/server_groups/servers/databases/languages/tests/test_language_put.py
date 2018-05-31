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

from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as language_utils


class TestLanguagesPut:
    def test_language_put(self, request, context_of_tests):
        """
        When the language put request is send to the backend
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

        data = \
            {
                "id": self.language_id,
                "description": "This is test comment."
            }
        response = self.tester.put("{0}{1}/{2}/{3}/{4}".format(
            url, utils.SERVER_GROUP, self.server_id, self.db_id,
            self.language_id), data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'language',
            'pgadmin.node.language',
            False,
            'icon-language',
            self.lang_name
        )

    def tearDown(self):
        language_utils.delete_language(
            self.server, self.db_name, self.lang_name
        )
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
