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
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_databases(['gpdb'])
class TestIndexConstraintAdd:
    @pytest.mark.usefixtures('require_database_connection')
    def test_primary_key_add(self, context_of_tests):
        """
        When the Primary Key add request is send
        to the backend
        It returns 200 status
        """
        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data['db_name']
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

        url = '/browser/primary_key/obj/'
        primary_key_name = 'test_primarykey_add_%s' % \
                           (str(uuid.uuid4())[1:8])
        primary_key_data = {'name': primary_key_name,
                            'spcname': 'pg_default',
                            'columns': [{'column': 'id'}]
                            }
        response = http_client.post(
            self.__build_url(server_data, table_id, url),
            data=json.dumps(primary_key_data),
            content_type='html/json')

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
    def test_uniquer_constraint_add(self, context_of_tests):
        """
        When the Unique Constraint add request is send to the backend
        It returns 200 status
        """
        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data['db_name']
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

        url = '/browser/unique_constraint/obj/'
        unique_key_name = 'test_uniquekey_add_%s' % \
                          (str(uuid.uuid4())[1:8])
        unique_key_data = {'name': unique_key_name,
                           'spcname': 'pg_default',
                           'columns': [{'column': 'id'}]}
        response = http_client.post(
            self.__build_url(server_data, table_id, url),
            data=json.dumps(unique_key_data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'unique_constraint',
            'pgadmin.node.unique_constraint',
            False,
            'icon-unique_constraint',
            unique_key_name
        )

    def __build_url(self, server_data, table_id, base_url):
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        schema_id = server_data['schema_id']
        return base_url + str(utils.SERVER_GROUP) + '/' + \
            str(server_id) + '/' + str(db_id) + \
            '/' + str(schema_id) + '/' + str(table_id) + '/'
