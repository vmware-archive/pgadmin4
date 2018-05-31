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

from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas. \
    fts_parser.tests import utils as fts_parser_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.schemas \
    .fts_configurations.tests import utils as fts_config_utils
from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


class TestFTSConfiguraionAdd:
    def test_fts_configuration_table_add(self, request, context_of_tests):
        """
        When the FTS configuration add request is send to the backend
        it returns 200 status
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/fts_configuration/obj/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]
        self.schema_name = self.schema_info['schema_name']
        self.schema_id = self.schema_info['schema_id']

        self.fts_parser_name = "fts_parser_%s" % str(uuid.uuid4())[1:8]
        self.fts_parser_id = fts_parser_utils.create_fts_parser(
            self.server, self.db_name, self.schema_name, self.fts_parser_name
        )

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

        self.fts_conf_name = "fts_conf_%s" % str(uuid.uuid4())[1:8]
        data = \
            {
                "name": self.fts_conf_name,
                "owner": self.server["username"],
                "prsname": "%s.%s" % (self.schema_name, self.fts_parser_name),
                "schema": self.schema_id,
                "tokens": []
            }

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.schema_id) + '/',
            data=json.dumps(data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'fts_configuration',
            'pgadmin.node.fts_configuration',
            False,
            'icon-fts_configuration',
            self.fts_conf_name
        )

    def tearDown(self):
        fts_config_utils.delete_fts_configurations(self.server, self.db_name,
                                                   self.schema_name,
                                                   self.fts_conf_name)
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
