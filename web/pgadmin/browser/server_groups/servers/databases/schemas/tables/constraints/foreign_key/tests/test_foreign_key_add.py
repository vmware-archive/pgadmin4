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


class TestForeignKeyAdd:
    @pytest.mark.usefixtures('require_database_connection')
    def test_constraint_add(self, context_of_tests):
        """
        When the foreign key add request is send to the backend
        it returns 200 status
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
            raise Exception('Could not find the schema to add a foreign '
                            'key constraint.')
        local_table_name = 'table_foreignkey_%s' % \
                           (str(uuid.uuid4())[1:8])
        local_table_id = tables_utils.create_table(server,
                                                   db_name,
                                                   schema_name,
                                                   local_table_name)
        foreign_table_name = 'table_foreignkey_%s' % \
                             (str(uuid.uuid4())[1:8])
        foreign_table_id = tables_utils.create_table(
            server, db_name, schema_name,
            foreign_table_name)

        foreignkey_name = 'test_foreignkey_add_%s' % \
                          (str(uuid.uuid4())[1:8])
        data = {'name': foreignkey_name,
                'columns': [{'local_column': 'id',
                             'references': foreign_table_id,
                             'referenced': 'id'}],
                'confupdtype': 'a', 'confdeltype': 'a', 'autoindex': False}

        response = http_client.post(
            self.__build_url(server_data, local_table_id),
            data=json.dumps(data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'foreign_key',
            'pgadmin.node.foreign_key',
            False,
            'icon-foreign_key',
            foreignkey_name
        )

    def __build_url(self, server_data, local_table_id):
        url = '/browser/foreign_key/obj/'
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        schema_id = server_data['schema_id']
        return url + str(utils.SERVER_GROUP) + '/' + \
            str(server_id) + '/' + str(db_id) + \
            '/' + str(schema_id) + '/' + str(local_table_id) + '/'
