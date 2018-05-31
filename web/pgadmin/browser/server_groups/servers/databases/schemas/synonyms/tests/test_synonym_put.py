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

from pgadmin.browser.server_groups.servers.databases.schemas.functions.tests \
    import utils as functions_utils
from pgadmin.browser.server_groups.servers.databases.schemas.sequences.tests \
    import utils as sequence_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.utils.base_test_generator import PostgresVersion
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression.python_test_utils import test_utils as utils
from . import utils as synonym_utils


@pytest.mark.skip_databases(['gpdb', 'pg'])
class TestSynonymUpdate:
    @pytest.mark.usefixtures('require_database_connection')
    def test_synonym_update(self,
                            context_of_tests,
                            get_server_version):
        """
        When the synonym PUT request is send to the backend
        it returns 200 status
        """

        url = '/browser/synonym/obj/'

        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        db_name = server_data['db_name']

        server_version = 0
        if PostgresVersion.v92 < get_server_version:
            server_version = get_server_version

        schema_name = server_data['schema_name']
        schema_id = server_data['schema_id']

        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception('Could not find the schema.')

        sequence_name = 'test_sequence_synonym_%s' % \
                        str(uuid.uuid4())[1:8]
        sequence_utils.create_sequences(
            server,
            db_name,
            schema_name,
            sequence_name
        )

        synonym_name = 'test_synonym_delete_%s' % str(uuid.uuid4())[1:8]
        synonym_utils.create_synonym(server,
                                     db_name,
                                     schema_name,
                                     synonym_name,
                                     sequence_name)
        synonym_response = synonym_utils.verify_synonym(server,
                                                        db_name,
                                                        synonym_name)
        if not synonym_response:
            raise Exception('No synonym node to update.')

        func_name = 'test_function_synonym_%s' % str(uuid.uuid4())[1:8]
        functions_utils.create_trigger_function(
            server,
            db_name,
            schema_name,
            func_name,
            server_version)

        data = {
            'name': synonym_name,
            'synobjname': func_name,
            'synobjschema': schema_name,
            'targettype': 'Function'
        }
        response = http_client.put(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' +
            str(db_id) + '/' +
            str(schema_id) + '/' +
            str(synonym_name),
            data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'synonym',
            'pgadmin.node.synonym',
            False,
            'icon-synonym',
            synonym_name
        )
