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
from . import utils as fk_utils


class TestForeignGet:
    @pytest.mark.usefixtures('require_database_connection')
    def test_foreign_key_get(self, context_of_tests):
        """
        When the check constraint GET request is send to the backend
        it returns 200 status
        """

        tester = context_of_tests['test_client']
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

        url = '/browser/foreign_key/obj/'
        response = tester.get(
            '{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(url,
                                                utils.SERVER_GROUP,
                                                server_id,
                                                db_id,
                                                schema_id,
                                                local_table_id,
                                                foreign_key_id),
            follow_redirects=True
        )

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('comment') > should.be.none
        (json_response | should.have.key('fknsp') >
         should.be.equal.to(schema_name))
        json_response | should.have.key('oid')
        json_response | should.have.key('name')
        (json_response | should.have.key('confdeltype') >
         should.be.equal.to('a'))
        (json_response | should.have.key('confkey') >
         should.be.equal.to([1]))
        json_response | should.have.key('confrelid')
        (json_response | should.have.key('reftab') >
         should.be.equal.to(foreign_table_name))
        json_response | should.have.key('condeferrable') > should.be.false
        json_response | should.have.key('condeferred') > should.be.false
        json_response | should.have.key('confmatchtype')
        (json_response | should.have.key('refnsp') >
         should.be.equal.to(schema_name))
        (json_response | should.have.key('fktab') >
         should.be.equal.to(local_table_name))
        json_response | should.have.key('hasindex') > should.be.true
        (json_response | should.have.key('conkey') >
         should.be.equal.to([1]))
        json_response | should.have.key('convalidated') > should.be.false
        json_response | should.have.key('autoindex') > should.be.true
        (json_response | should.have.key('fktab') >
         should.be.equal.to(local_table_name))
        json_response | should.have.key('coveringindex')

        json_response | should.have.key('columns')
        (json_response['columns'][0] | should.have.key('referenced') >
         should.be.equal.to('id'))
        json_response['columns'][0] | should.have.key('references')
        (json_response['columns'][0] | should.have.key('local_column') >
         should.be.equal.to('id'))
