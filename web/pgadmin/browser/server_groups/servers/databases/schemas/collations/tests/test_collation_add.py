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
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_databases(['gpdb'])
class TestCollationAdd:
    def test_collation_add(self, request, context_of_tests):
        """
        When the collation add request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/collation/obj/'

        self.server_data = parent_node_dict['database'][-1]
        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        schema_data = context_of_tests['server_information']
        self.db_name = schema_data["db_name"]
        self.schema_name = "schema_get_%s" % str(uuid.uuid4())[1:8]

        connection = utils.get_db_connection(self.db_name,
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        self.schema_details = schema_utils.create_schema(connection,
                                                         self.schema_name)

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        schema_id = self.schema_details[0]
        schema_name = self.schema_details[1]
        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema to add the collation.")

        collation_name = "collation_add_%s" % str(uuid.uuid4())[1:8]
        data = {
            "copy_collation": "pg_catalog.\"C\"",
            "name": collation_name,
            "owner": self.server["username"],
            "schema": schema_name
        }
        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) + '/' +
            str(schema_id) + '/',
            data=json.dumps(data),
            content_type='html/json')
        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'collation',
            'pgadmin.node.collation',
            False,
            'icon-collation',
            collation_name
        )

    def tearDown(self):
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
