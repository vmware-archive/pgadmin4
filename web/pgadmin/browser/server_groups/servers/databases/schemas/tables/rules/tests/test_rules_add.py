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

from pgadmin.browser.server_groups.servers.databases.schemas.tables.tests \
    import utils as tables_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression.python_test_utils import test_utils as utils


class TestRulesAdd:
    @pytest.mark.usefixtures('require_database_connection')
    def test_rule_add(self, context_of_tests):
        """
        When the rule add request is send to the backend
        it returns 200 status
        """
        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data['db_name']
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        schema_id = server_data['schema_id']
        schema_name = server_data['schema_name']
        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception('Could not find the schema to add a rule.')
        table_name = 'table_column_%s' % (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server, db_name,
                                             schema_name,
                                             table_name)

        rule_name = 'test_rule_add_%s' % (str(uuid.uuid4())[1:8])
        data = {'schema': schema_name,
                'view': table_name,
                'name': rule_name,
                'event': 'Update'
                }
        url = '/browser/rule/obj/'
        response = http_client.post(
            '{0}{1}/{2}/{3}/{4}/{5}/'.format(url, utils.SERVER_GROUP,
                                             server_id, db_id,
                                             schema_id, table_id),
            data=json.dumps(data),
            content_type='html/json'
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'rule',
            'pgadmin.node.rule',
            False,
            'icon-rule',
            rule_name
        )
