##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import sys

from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas.utils import \
    DataTypeReader
from pgadmin.utils.base_test_generator import BaseTestGenerator

if sys.version_info < (3, 3):
    from mock import patch, Mock
else:
    from unittest.mock import patch, Mock

_default_database_response = [
    {
        'typname': 'type name',
        'elemoid': 1560,
        'is_collatable': True
    }
]
_default_expected_function_output = [
    {
        'label': 'type name',
        'value': 'type name',
        'typval': 'L',
        'precision': False,
        'length': True,
        'min_val': 1,
        'max_val': 2147483647,
        'is_collatable': True
    }
]
_default_manager = dict(
    server_type='ppas',
    version='456'
)


class TestDataTypeReader(BaseTestGenerator):

    @patch('pgadmin.browser.server_groups.servers.databases.schemas.utils'
           '.render_template')
    def test_schema_oid(self, template_mock):
        """Schema Oid is passed to the SQL Renderer"""
        manager = _default_manager
        sql_condition = 'new condition'
        schema_oid = '123'
        add_serials = False
        expected_sql_template_path = 'someplate/where/templates/are'
        expected_function_output = _default_expected_function_output
        template_mock.return_value = 'Some SQL'
        connection = Mock()
        connection.execute_2darray.return_value = [
            True,
            {
                'rows': _default_database_response

            }
        ]
        reader = DataTypeReader()
        reader.manager = Mock()
        reader.manager.server_type = manager['server_type']
        reader.manager.version = manager['version']
        try:
            reader.data_type_template_path = 'someplate/where/templates/are'
        except AttributeError:
            ''

        result = reader.get_types(
            connection,
            sql_condition,
            add_serials,
            schema_oid
        )

        result | should.have.length.of(2)
        result[1] | should.be.equal.to(expected_function_output)
        result[0] | should.be.true

        connection.execute_2darray.assert_called_with('Some SQL')
        template_mock.assert_called_with(
            expected_sql_template_path + '/get_types.sql',
            condition=sql_condition,
            add_serials=add_serials,
            schema_oid=schema_oid
        )

    @patch('pgadmin.browser.server_groups.servers.databases.schemas.utils'
           '.render_template')
    def test_no_data_type_template_path(self, template_mock):
        """
        When no data_type_template_path is present in class,
        should create template path with version number
        """
        manager = _default_manager
        sql_condition = 'new condition'
        schema_oid = '123'
        add_serials = False
        expected_sql_template_path = 'datatype/sql/#456#'
        expected_function_output = _default_expected_function_output
        template_mock.return_value = 'Some SQL'
        connection = Mock()
        connection.execute_2darray.return_value = [
            True,
            {
                'rows': _default_database_response

            }
        ]
        reader = DataTypeReader()
        reader.manager = Mock()
        reader.manager.server_type = manager['server_type']
        reader.manager.version = manager['version']

        result = reader.get_types(
            connection,
            sql_condition,
            add_serials,
            schema_oid
        )

        result | should.have.length.of(2)
        result[1] | should.be.equal.to(expected_function_output)
        result[0] | should.be.true

        connection.execute_2darray.assert_called_with('Some SQL')
        template_mock.assert_called_with(
            expected_sql_template_path + '/get_types.sql',
            condition=sql_condition,
            add_serials=add_serials,
            schema_oid=schema_oid
        )

    @patch('pgadmin.browser.server_groups.servers.databases.schemas.utils'
           '.render_template')
    def test_no_data_type_template_path_for_gpdb(self, template_mock):
        """
        When no data_type_template_path is present in class for GreenPlum,
        should create template path with gpdb and the version number
        """
        manager = dict(server_type='gpdb', version='456')
        sql_condition = 'new condition'
        schema_oid = '123'
        add_serials = False
        expected_sql_template_path = 'datatype/sql/#gpdb#456#'
        expected_function_output = _default_expected_function_output
        template_mock.return_value = 'Some SQL'
        connection = Mock()
        connection.execute_2darray.return_value = [
            True,
            {
                'rows': _default_database_response

            }
        ]
        reader = DataTypeReader()
        reader.manager = Mock()
        reader.manager.server_type = manager['server_type']
        reader.manager.version = manager['version']

        result = reader.get_types(
            connection,
            sql_condition,
            add_serials,
            schema_oid
        )

        result | should.have.length.of(2)
        result[1] | should.be.equal.to(expected_function_output)
        result[0] | should.be.true

        connection.execute_2darray.assert_called_with('Some SQL')
        template_mock.assert_called_with(
            expected_sql_template_path + '/get_types.sql',
            condition=sql_condition,
            add_serials=add_serials,
            schema_oid=schema_oid
        )
