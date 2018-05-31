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
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as language_utils


@pytest.mark.skip_databases(['gpdb'])
class TestLanguagesAdd:
    def test_language_add(self, request, context_of_tests):
        """
        When the language add request is send to the backend
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
        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        db_user = self.server['username']
        self.data = {
            "lanacl": [],
            "laninl": "btint2sortsupport",
            "lanowner": db_user,
            "lanproc": "plpgsql_call_handler",
            "lanval": "fmgr_c_validator",
            "name": "language_%s" % str(uuid.uuid4())[1:8],
            "seclabels": [],
            "template_list": [
                "plperl",
                "plperlu",
                "plpython2u",
                "plpython3u",
                "plpythonu",
                "pltcl",
                "pltclu"
            ],
            "trusted": "true"
        }

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'language',
            'pgadmin.node.language',
            False,
            'icon-language',
            self.data['name']
        )

    def tearDown(self):
        language_utils.delete_language(
            self.server, self.db_name, self.data['name']
        )
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
