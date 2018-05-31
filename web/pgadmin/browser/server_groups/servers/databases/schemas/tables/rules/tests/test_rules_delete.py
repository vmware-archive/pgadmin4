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

from pgadmin.browser.server_groups.servers.databases.schemas.tables.tests \
    import utils as tables_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as rules_utils


class TestRulesDelete:
    @pytest.mark.usefixtures('require_database_connection')
    def test_rule_delete(self, context_of_tests):
        """
        When the rule DELETE request is send to the backend
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
            raise Exception('Could not find the rule to delete.')
        url = '/browser/rule/obj/'
        response = http_client.delete(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id, table_id,
                                                rule_id),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Rule dropped')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)
