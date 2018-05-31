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

from pgadmin.browser.server_groups.servers.databases.event_triggers \
    .tests.event_trigger_test_base_class import EventTriggerTestBaseClass
from pgadmin.utils.base_test_generator import PostgresVersion
from regression import trigger_funcs_utils
from regression.python_test_utils import test_utils as utils
from . import utils as event_trigger_utils


@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v93},
                                      "Event triggers are not supported "
                                      "by PG9.2 "
                                      "and PPAS9.2 and below.")
class TestEventTriggerGet(EventTriggerTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup, context_of_tests):
        self.func_name = "trigger_func_%s" % str(uuid.uuid4())[1:8]
        super(TestEventTriggerGet, self).setUp(context_of_tests)

        self.trigger_name = "event_trigger_get_%s" % (
            str(uuid.uuid4())[1:8])
        self.event_trigger_id = event_trigger_utils.create_event_trigger(
            self.server, self.db_name, self.schema_name, self.func_name,
            self.trigger_name)

    def test_get(self):
        """ When a trigger exists
         When schema exist
         When backend receives a request to retrieve a trigger information
         It returns trigger information"""
        url = '/browser/event_trigger/obj/'

        self._is_schema_and_database_available()

        func_name = self.function_info[1]
        func_response = trigger_funcs_utils.verify_trigger_function(
            self.server,
            self.db_name,
            func_name)
        if not func_response:
            raise Exception("Could not find the trigger function.")

        response = self.tester.get(
            url +
            str(utils.SERVER_GROUP) + '/' + str(self.server_id) + '/' +
            str(self.db_id) + '/' + str(self.event_trigger_id),
            content_type='html/json'
        )

        response.status_code | should.be.equal.to(200)
        json_response = self.response_to_json(response)

        json_response | should.have.key('schemaoid')
        json_response | should.have.key('eventfunname')
        json_response | should.have.key('oid')
        json_response | should.have.key('eventfuncoid')
        json_response | should.have.key('xmin')

        (json_response | should.have.key('comment') >
         should.be.equal.to(None))
        (json_response | should.have.key('name') >
         should.be.equal.to(self.trigger_name))
        (json_response | should.have.key('language') >
         should.be.equal.to('plpgsql'))
        (json_response | should.have.key('when') >
         should.be.empty)
        (json_response | should.have.key('enabled') >
         should.be.equal.to('O'))
        (json_response | should.have.key('eventowner') >
         should.be.equal.to(self.db_user))
        (json_response | should.have.key('eventname') >
         should.be.equal.to('DDL_COMMAND_END'))
        (json_response | should.have.key('source') >
         should.be.equal.to(' BEGIN NULL; END; '))
        (json_response | should.have.key('seclabels') >
         should.be.empty)
