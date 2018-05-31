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
from . import utils as rules_utils


class TestRulesUpdate:
    @pytest.mark.usefixtures('require_database_connection')
    def test_rule_update(self, context_of_tests):
        """
        When the rule PUT request is send to the backend
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
            raise Exception('Could not find the schema to delete rule.')
        table_name = 'table_column_%s' % (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server, db_name,
                                             schema_name,
                                             table_name)
        rule_name = 'test_rule_delete_%s' % (str(uuid.uuid4())[1:8])
        rule_id = rules_utils.create_rule(server, db_name,
                                          schema_name,
                                          table_name,
                                          rule_name)
        rule_response = rules_utils.verify_rule(server, db_name,
                                                rule_name)
        if not rule_response:
            raise Exception('Could not find the rule to update.')

        data = {'id': rule_id,
                'comment': 'This is testing comment.'
                }
        url = '/browser/rule/obj/'
        response = http_client.put(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id, table_id,
                                                rule_id),
            data=json.dumps(data),
            follow_redirects=True)

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
