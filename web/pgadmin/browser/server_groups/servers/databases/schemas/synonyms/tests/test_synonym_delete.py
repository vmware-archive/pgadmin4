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

from pgadmin.browser.server_groups.servers.databases.schemas.sequences.tests \
    import utils as sequence_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils.tests_helper import convert_response_to_json
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as synonym_utils


@pytest.mark.skip_databases(['gpdb', 'pg'])
class TestSynonymDelete:
    @pytest.mark.usefixtures('require_database_connection')
    def test_synonym_delete(self, context_of_tests):
        """
        When the synonym DELETE request is send to the backend
        it returns 200 status
        """

        url = '/browser/synonym/obj/'

        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        db_name = server_data['db_name']

        schema_name = server_data['schema_name']
        schema_id = server_data['schema_id']
        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        sequence_name = "test_sequence_synonym_%s" % \
                        str(uuid.uuid4())[1:8]
        sequence_utils.create_sequences(
            server,
            db_name,
            schema_name,
            sequence_name
        )

        synonym_name = "test_synonym_delete_%s" % str(uuid.uuid4())[1:8]
        synonym_utils.create_synonym(server,
                                     db_name,
                                     schema_name,
                                     synonym_name,
                                     sequence_name)
        synonym_response = synonym_utils.verify_synonym(server,
                                                        db_name,
                                                        synonym_name)
        if not synonym_response:
            raise Exception("No synonym node to delete.")

        response = http_client.delete(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' +
            str(db_id) + '/' +
            str(schema_id) + '/' +
            str(synonym_name),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('info') > should.be.equal.to(
            'Synonym dropped')
        json_response | should.have.key('errormsg') > should.be.empty
        json_response | should.have.key('data')
        json_response | should.have.key('result') > should.be.none
        json_response | should.have.key('success') > should.be.equal.to(1)
