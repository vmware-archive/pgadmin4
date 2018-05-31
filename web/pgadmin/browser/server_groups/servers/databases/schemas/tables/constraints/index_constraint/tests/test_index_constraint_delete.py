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
from . import utils as index_constraint_utils


@pytest.mark.skip_databases(['gpdb'])
class TestIndexConstraintDelete:
    @pytest.mark.usefixtures('require_database_connection')
    def test_primary_key_delete(self, context_of_tests):
        """
        When the Primary Key Constraint DELETE request is send to the backend
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

        primary_key_name = 'test_primarykey_delete_%s' % \
                           (str(uuid.uuid4())[1:8])
        index_constraint_id = \
            index_constraint_utils.create_index_constraint(
                server, db_name, schema_name, table_name,
                primary_key_name, 'PRIMARY KEY')
        url = '/browser/primary_key/obj/'

        response = http_client.delete(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id,
                                                table_id,
                                                index_constraint_id),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Primary key dropped.')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)

    @pytest.mark.usefixtures('require_database_connection')
    def test_unique_constraint_delete(self, context_of_tests):
        """
        When the Unique Constraint DELETE request is send to the backend
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

        unique_constraint_name = 'test_uniquekey_delete_%s' % \
                                 (str(uuid.uuid4())[1:8])
        index_constraint_id = \
            index_constraint_utils.create_index_constraint(
                server, db_name, schema_name, table_name,
                unique_constraint_name, 'UNIQUE')
        url = '/browser/unique_constraint/obj/'

        response = http_client.delete(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id,
                                                table_id,
                                                index_constraint_id),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Unique constraint dropped.')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)
