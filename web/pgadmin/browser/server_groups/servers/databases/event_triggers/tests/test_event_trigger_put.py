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
from . import utils as event_trigger_utils


@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v93},
                                      "Event triggers are not supported "
                                      "by PG9.2 "
                                      "and PPAS9.2 and below.")
class TestEventTriggerPut(EventTriggerTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup, context_of_tests):
        self.func_name = "trigger_func_%s" % str(uuid.uuid4())[1:8]
        super(TestEventTriggerPut, self).setUp(context_of_tests)

        self.trigger_name = "event_trigger_put_%s" % (str(uuid.uuid4())[1:8])
        self.event_trigger_id = event_trigger_utils.create_event_trigger(
            self.server, self.db_name, self.schema_name, self.func_name,
            self.trigger_name)

    def test_put(self):
        """ When a trigger exists
         When schema exist
         When backend receives a valid request to update a trigger
         It updates the trigger information
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
        trigger_response = event_trigger_utils.verify_event_trigger(
            self.server, self.db_name, self.trigger_name)
        if not trigger_response:
            raise Exception("Could not find event trigger.")
        data = {
            "comment": "This is event trigger update comment",
            "id": self.event_trigger_id
        }
        put_response = self.tester.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.event_trigger_id),
            data=json.dumps(data),
            follow_redirects=True)

        put_response.status_code | should.be.equal.to(200)

        json_response = self.response_to_json(put_response)
        self.assert_node_json(json_response,
                              'event_trigger',
                              'pgadmin.node.event_trigger',
                              False,
                              'icon-event_trigger',
                              self.trigger_name)
