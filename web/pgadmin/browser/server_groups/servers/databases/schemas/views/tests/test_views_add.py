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
from pgadmin.utils.base_test_generator import PostgresVersion
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v93},
                                      "Materialized Views are not supported "
                                      "by PG9.2 "
                                      "and PPAS9.2 and below.")
class TestViewAdd:
    def test_views_add(self, request, context_of_tests):
        """
        When the views add request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/view/obj/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]
        self.schema_name = self.schema_info['schema_name']
        self.schema_id = self.schema_info['schema_id']

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
        view_name = "test_view_add_%s" % (str(uuid.uuid4())[1:8])
        data = {
            "schema": self.schema_name,
            "owner": db_user,
            "datacl": [],
            "seclabels": [],
            "name": view_name,
            "definition": "SELECT 'Hello World';"
        }

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
            'view',
            'pgadmin.node.view',
            True,
            'icon-view',
            view_name
        )

    def test_materialized_views_add(self, request, context_of_tests):
        """
        When the materialized views add request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/mview/obj/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]
        self.schema_name = self.schema_info['schema_name']
        self.schema_id = self.schema_info['schema_id']

        server_response = server_utils.connect_server(self, self.server_id)

        if server_response["data"]["version"] < 90300:
            message = "Materialized Views are not supported by PG9.2 " \
                      "and PPAS9.2 and below."
            pytest.skipTest(message)

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
        view_name = "test_mview_add_%s" % (str(uuid.uuid4())[1:8])
        data = {
            "spcname": "pg_default",
            "toast_autovacuum_enabled": False,
            "autovacuum_enabled": False,
            "schema": self.schema_name,
            "owner": db_user,
            "vacuum_table": [
                {"name": "autovacuum_analyze_scale_factor"},
                {"name": "autovacuum_analyze_threshold"},
                {"name": "autovacuum_freeze_max_age"},
                {"name": "autovacuum_vacuum_cost_delay"},
                {"name": "autovacuum_vacuum_cost_limit"},
                {"name": "autovacuum_vacuum_scale_factor"},
                {"name": "autovacuum_vacuum_threshold"},
                {"name": "autovacuum_freeze_min_age"},
                {"name": "autovacuum_freeze_table_age"}],
            "vacuum_toast": [{"name": "autovacuum_freeze_max_age"},
                             {"name": "autovacuum_vacuum_cost_delay"},
                             {"name": "autovacuum_vacuum_cost_limit"},
                             {"name": "autovacuum_vacuum_scale_factor"},
                             {"name": "autovacuum_vacuum_threshold"},
                             {"name": "autovacuum_freeze_min_age"},
                             {"name": "autovacuum_freeze_table_age"}],
            "datacl": [],
            "seclabels": [],
            "name": view_name,
            "definition": "SELECT 'test_pgadmin';"
        }

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
            'mview',
            'pgadmin.node.mview',
            True,
            'icon-view',
            view_name
        )

    def tearDown(self):
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
