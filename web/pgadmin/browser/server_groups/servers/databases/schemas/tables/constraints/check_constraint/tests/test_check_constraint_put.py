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
from . import utils as chk_constraint_utils


@pytest.mark.skip_databases(['gpdb'])
class TestCheckConstraintPut:
    @pytest.mark.usefixtures('require_database_connection')
    def test_check_constraint_update(self, context_of_tests):
        """
        When the check constraint PUT request is send to the backend
        it returns 200 status
        """
        url = '/browser/check_constraint/obj/'

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
            raise Exception('Could not find the schema to update a check '
                            'constraint.')

        table_name = 'table_checkconstraint_put_%s' % \
                     (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server,
                                             db_name,
                                             schema_name,
                                             table_name)
        check_constraint_name = 'test_checkconstraint_put_%s' % \
                                (str(uuid.uuid4())[1:8])
        check_constraint_id = \
            chk_constraint_utils.create_check_constraint(
                server, db_name, schema_name, table_name,
                check_constraint_name)

        chk_constraint = chk_constraint_utils.verify_check_constraint(
            server, db_name, check_constraint_name)
        if not chk_constraint:
            raise Exception('Could not find the check constraint to update.')
        data = {'oid': check_constraint_id,
                'comment': 'This is test comment for check constraint.'}
        response = http_client.put(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id,
                                                table_id,
                                                check_constraint_id),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'check_constraint',
            'pgadmin.node.check_constraint',
            False,
            'icon-check_constraint_bad',
            check_constraint_name
        )
