##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils import server_utils as server_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_databases(['gpdb'])
class TestTriggerFunctionsAdd:
    def test_trigger_functions_add(self, request, context_of_tests):
        """
        When the Trigger Functions add request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/trigger_function/obj/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]
        self.schema_name = self.schema_info['schema_name']
        self.schema_id = self.schema_info['schema_id']

        prorettypename = "event_trigger/trigger"
        server_con = server_utils.connect_server(self, self.server_id)
        if not server_con["info"] == "Server connected.":
            raise Exception("Could not connect to server to add resource "
                            "groups.")
        if "type" in server_con["data"]:
            if server_con["data"]["version"] < 90300:
                prorettypename = "trigger"

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      self.schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        db_user = self.server["username"]
        data = {
            "acl": [
                {
                    "grantee": db_user,
                    "grantor": db_user,
                    "privileges":
                        [
                            {
                                "privilege_type": "X",
                                "privilege": True,
                                "with_grant": True
                            }
                        ]
                }
            ],
            "arguments": [],
            "funcowner": db_user,
            "lanname": "plpgsql",
            "name": "test_abort_any_command",
            "options": [],
            "proleakproof": True,
            "pronamespace": 2200,
            "prorettypename": prorettypename,
            "prosecdef": True,
            "prosrc": "BEGIN RAISE EXCEPTION 'command % is disabled',"
                      " tg_tag; END;",
            "provolatile": "s",
            "seclabels": [],
            "variables": [
                {
                    "name": "enable_sort",
                    "value": True
                }
            ]
        }
        # Get the type from data. We are adding two types
        # i.e. event_trigger and trigger.
        trigger_func_types = data['prorettypename'].split('/')
        for func_type in trigger_func_types:
            data['prorettypename'] = func_type
            trigger_func_name = \
                "test_event_add_%s" % str(uuid.uuid4())[1:8]
            data["name"] = trigger_func_name
            if self.schema_id:
                data['pronamespace'] = self.schema_id
            else:
                self.schema_id = data['pronamespace']
            response = self.tester.post(
                url + str(utils.SERVER_GROUP) + '/' +
                str(self.server_id) + '/' +
                str(self.db_id) + '/' +
                str(self.schema_id) + '/',
                data=json.dumps(data),
                content_type='html/json')

            response.status_code | should.be.equal.to(200)
            json_response = convert_response_to_json(response)
            assert_json_values_from_response(
                json_response,
                'trigger_function',
                'pgadmin.node.trigger_function',
                False,
                'icon-trigger_function',
                trigger_func_name + '()'
            )

    def tearDown(self):
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
