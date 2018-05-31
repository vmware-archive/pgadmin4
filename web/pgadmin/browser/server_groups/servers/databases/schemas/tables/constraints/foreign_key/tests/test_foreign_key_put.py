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
from . import utils as fk_utils


class TestForeignKeyPut:
    @pytest.mark.usefixtures('require_database_connection')
    def test_foreign_key_update(self, context_of_tests):
        """
        When the foreign keys PUT request is send to the backend
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
            raise Exception('Could not find the schema to fetch a foreign '
                            'key constraint.')
        local_table_name = 'local_table_foreignkey_get_%s' % \
                           (str(uuid.uuid4())[1:8])
        local_table_id = tables_utils.create_table(
            server, db_name, schema_name, local_table_name)
        foreign_table_name = 'foreign_table_foreignkey_get_%s' % \
                             (str(uuid.uuid4())[1:8])
        tables_utils.create_table(
            server, db_name, schema_name,
            foreign_table_name)
        foreign_key_id = fk_utils.create_foreignkey(
            server, db_name, schema_name, local_table_name,
            foreign_table_name)

        data = {'oid': foreign_key_id,
                'comment': 'This is TEST comment for foreign key constraint.'
                }

        url = '/browser/foreign_key/obj/'
        response = http_client.put(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id,
                                                local_table_id,
                                                foreign_key_id),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'foreign_key',
            'pgadmin.node.foreign_key',
            False,
            'icon-foreign_key',
            local_table_name + '_id_fkey'
        )
