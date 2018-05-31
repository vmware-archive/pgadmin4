##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

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
class TestEventTriggerDelete(EventTriggerTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup, context_of_tests):
        self.func_name = "trigger_func_%s" % str(uuid.uuid4())[1:8]
        super(TestEventTriggerDelete, self).setUp(context_of_tests)

        self.trigger_name = "event_trigger_delete_%s" % (
            str(uuid.uuid4())[1:8])
        self.event_trigger_id = event_trigger_utils.create_event_trigger(
            self.server, self.db_name, self.schema_name, self.func_name,
            self.trigger_name)

    def test_delete(self):
        """ When a trigger exists
         When schema exist
         When backend receives a request to remove a trigger
         It removes the trigger
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
            self.server, self.db_name,
            self.trigger_name)
        if not trigger_response:
            raise Exception("Could not find event trigger.")

        del_response = self.tester.delete(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' +
            str(self.event_trigger_id),
            follow_redirects=True)

        del_response.status_code | should.be.equal.to(200)
        json_response = self.response_to_json(del_response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Event trigger dropped')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)
