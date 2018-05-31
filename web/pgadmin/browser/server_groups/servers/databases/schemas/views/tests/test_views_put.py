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
from . import utils as views_utils


class TestViewGet:
    def test_views_get(self, request, context_of_tests):
        """
        When the views get request is send to the backend
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

        view_name = "test_view_delete_%s" % (str(uuid.uuid4())[1:8])
        sql_query = "CREATE OR REPLACE VIEW %s.%s AS SELECT 'Hello World'; " \
                    "ALTER TABLE %s.%s OWNER TO %s"
        self.view_id = views_utils.create_view(self.server,
                                               self.db_name,
                                               self.schema_name,
                                               sql_query,
                                               view_name)
        view_response = views_utils.verify_view(self.server, self.db_name,
                                                view_name)
        if not view_response:
            raise Exception("Could not find the view to update.")

        data = {
            "id": self.view_id,
            "comment": "This is test comment"
        }
        response = self.tester.put(
            "{0}{1}/{2}/{3}/{4}/{5}".format(url, utils.SERVER_GROUP,
                                            self.server_id, self.db_id,
                                            self.schema_id, self.view_id
                                            ),
            data=json.dumps(data),
            follow_redirects=True)

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

    @pytest.mark.skip_if_postgres_version(
        {'below_version': PostgresVersion.v93},
        "Materialized Views are not supported "
        "by PG9.2 "
        "and PPAS9.2 and below.")
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

        view_name = "test_mview_delete_%s" % (str(uuid.uuid4())[1:8])
        sql_query = "CREATE MATERIALIZED VIEW %s.%s TABLESPACE" \
                    " pg_default AS " \
                    "SELECT 'test_pgadmin' WITH NO DATA;" \
                    "ALTER TABLE %s.%s OWNER" \
                    " TO %s"
        self.view_id = views_utils.create_view(self.server,
                                               self.db_name,
                                               self.schema_name,
                                               sql_query,
                                               view_name)
        view_response = views_utils.verify_view(self.server, self.db_name,
                                                view_name)
        if not view_response:
            raise Exception("Could not find the view to update.")

        data = {
            "id": self.view_id,
            "comment": "This is test comment"
        }
        response = self.tester.put(
            "{0}{1}/{2}/{3}/{4}/{5}".format(url, utils.SERVER_GROUP,
                                            self.server_id, self.db_id,
                                            self.schema_id, self.view_id
                                            ),
            data=json.dumps(data),
            follow_redirects=True)

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
