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
from . import utils as index_constraint_utils


@pytest.mark.skip_databases(['gpdb'])
class TestIndexConstraintUpdate:
    @pytest.mark.usefixtures('require_database_connection')
    def test_primary_key_update(self, context_of_tests):
        """
        When the Primary Key PUT request is send to the backend
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
            raise Exception('Could not find the schema to add a index '
                            'constraint(primary key or unique key).')
        table_name = 'table_indexconstraint_%s' % \
                     (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server,
                                             db_name,
                                             schema_name,
                                             table_name)
        primary_key_name = 'test_primarykey_put_%s' % \
                           (str(uuid.uuid4())[1:8])
        index_constraint_id = \
            index_constraint_utils.create_index_constraint(
                server, db_name, schema_name, table_name,
                primary_key_name, 'PRIMARY KEY')
        data = {'oid': index_constraint_id, 'comment': 'this is test comment'}
        url = '/browser/primary_key/obj/'
        response = http_client.put(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url,
                                                utils.SERVER_GROUP,
                                                server_id,
                                                db_id,
                                                schema_id,
                                                table_id,
                                                index_constraint_id
                                                ),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'primary_key',
            'pgadmin.node.primary_key',
            False,
            'icon-primary_key',
            primary_key_name
        )

    @pytest.mark.usefixtures('require_database_connection')
    def test_unique_constraint_update(self, context_of_tests):
        """
        When the Unique Constraint PUT request is send to the backend
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
            raise Exception('Could not find the schema to add a index '
                            'constraint(primary key or unique key).')
        table_name = 'table_indexconstraint_%s' % \
                     (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server,
                                             db_name,
                                             schema_name,
                                             table_name)
        unique_constraint_name = 'test_uniqueconstraint_put_%s' % \
                                 (str(uuid.uuid4())[1:8])
        index_constraint_id = \
            index_constraint_utils.create_index_constraint(
                server, db_name, schema_name, table_name,
                unique_constraint_name, 'UNIQUE')
        data = {'oid': index_constraint_id, 'comment': 'this is test comment'}
        url = '/browser/unique_constraint/obj/'
        response = http_client.put(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url,
                                                utils.SERVER_GROUP,
                                                server_id,
                                                db_id,
                                                schema_id,
                                                table_id,
                                                index_constraint_id
                                                ),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'unique_constraint',
            'pgadmin.node.unique_constraint',
            False,
            'icon-unique_constraint',
            unique_constraint_name
        )
