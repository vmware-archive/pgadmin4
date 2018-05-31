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

from pgadmin.browser.server_groups.servers.databases.event_triggers\
    .tests.event_trigger_test_base_class import EventTriggerTestBaseClass
from pgadmin.utils.base_test_generator import PostgresVersion
from regression import trigger_funcs_utils
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v93},
                                      "Event triggers are not supported "
                                      "by PG9.2 "
                                      "and PPAS9.2 and below.")
class TestEventTriggerAdd(EventTriggerTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup, context_of_tests):
        self.func_name = "trigger_func_%s" % str(uuid.uuid4())[1:8]
        super(TestEventTriggerAdd, self).setUp(context_of_tests)

    def test_add_trigger(self):
        """ When a trigger function exists
         When schema exist
         When backend receives a valid request to create a new trigger
         It creates the trigger
         And returns success 200"""
        url = '/browser/event_trigger/obj/'

        self._is_schema_and_database_available()

        func_name = self.function_info[1]
        func_response = trigger_funcs_utils.verify_trigger_function(
            self.server,
            self.db_name,
            func_name)
        if not func_response:
            raise Exception("Could not find the trigger function.")
        data = {
            "enabled": "O",
            "eventfunname": "%s.%s" % (self.schema_name, self.func_name),
            "eventname": "DDL_COMMAND_END",
            "eventowner": self.db_user,
            "name": "event_trigger_add_%s" % (str(uuid.uuid4())[1:8]),
            "providers": []
        }

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/', data=json.dumps(data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = self.response_to_json(response)

        self.assert_node_json(json_response,
                              'event_trigger',
                              'pgadmin.node.event_trigger',
                              False,
                              'icon-event_trigger',
                              data['name'])
