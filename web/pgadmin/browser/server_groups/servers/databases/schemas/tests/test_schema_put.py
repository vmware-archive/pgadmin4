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

from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as schema_utils


@pytest.mark.skip_databases(['gpdb'])
class TestSchemaPut:
    def test_schema_put(self, request, context_of_tests):
        """
        When the schema put request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/schema/obj/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        self.schema_name = "schema_get_%s" % str(uuid.uuid4())[1:8]
        connection = utils.get_db_connection(self.db_name,
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        self.schema_details = schema_utils.create_schema(connection,
                                                         self.schema_name)
        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      self.schema_name)
        if not schema_response:
            raise Exception("Could not find the schema to update.")

        self.schema_id = self.schema_details[0]
        db_user = self.server["username"]
        data = {
            "deffuncacl": {
                "added":
                    [
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
                    ]
            },
            "defseqacl": {
                "added":
                    [
                        {
                            "grantee": db_user,
                            "grantor": db_user,
                            "privileges":
                                [
                                    {
                                        "privilege_type": "r",
                                        "privilege": True,
                                        "with_grant": False
                                    },
                                    {
                                        "privilege_type": "w",
                                        "privilege": True,
                                        "with_grant": False
                                    },
                                    {
                                        "privilege_type": "U",
                                        "privilege": True,
                                        "with_grant": False
                                    }
                                ]
                        }
                    ]
            },
            "deftblacl": {
                "added":
                    [
                        {
                            "grantee": "public",
                            "grantor": db_user,
                            "privileges":
                                [
                                    {
                                        "privilege_type": "D",
                                        "privilege": True,
                                        "with_grant": False
                                    },
                                    {
                                        "privilege_type": "x",
                                        "privilege": True,
                                        "with_grant": False
                                    }
                                ]
                        }
                    ]
            },
            "id": self.schema_id
        }

        response = self.tester.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' +
            str(self.schema_id),
            data=json.dumps(data), follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        print(json_response)
        assert_json_values_from_response(
            json_response,
            'schema',
            'pgadmin.node.schema',
            True,
            'icon-schema',
            self.schema_name
        )

    def tearDown(self):
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
