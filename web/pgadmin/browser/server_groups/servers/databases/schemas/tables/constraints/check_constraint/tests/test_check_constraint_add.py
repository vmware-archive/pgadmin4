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
from pgadmin.utils.tests_helper import assert_json_values_from_response, \
    convert_response_to_json
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_databases(['gpdb'])
class TestCheckConstraintAdd:
    @pytest.mark.usefixtures('require_database_connection')
    def test_constraint_add(self, context_of_tests):
        """
        When the constraint add request is send to the backend
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
            raise Exception('Could not find the schema to add a check '
                            'constraint.')
        table_name = 'table_checkconstraint_add_%s' % \
                     (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server,
                                             db_name,
                                             schema_name,
                                             table_name)

        check_constraint_name = 'test_checkconstraint_add_%s' % \
                                (str(uuid.uuid4())[1:8])
        data = {'name': check_constraint_name,
                'consrc': ' (id > 0)',
                'convalidated': True,
                'comment': 'this is test comment'}
        response = http_client.post(
            self.__build_url(server_data, table_id),
            data=json.dumps(data),
            content_type='html/json')

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

    def __build_url(self, server_information, table_id):
        url = '/browser/check_constraint/obj/'
        server_id = server_information['server_id']
        db_id = server_information['db_id']
        schema_id = server_information['schema_id']

        return url + str(utils.SERVER_GROUP) + '/' + \
            str(server_id) + '/' + str(db_id) + \
            '/' + str(schema_id) + '/' + str(table_id) + '/'
