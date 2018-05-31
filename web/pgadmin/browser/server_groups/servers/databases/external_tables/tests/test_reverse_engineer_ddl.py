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

from pgadmin.browser.server_groups.servers.databases \
    .external_tables.reverse_engineer_ddl import \
    ReverseEngineerDDL, ReverseEngineerDDLException

if sys.version_info < (3, 3):
    from mock import MagicMock
else:
    from unittest.mock import MagicMock


class TestReverseEngineerDDL:
    def test_execute(self):
        """
        When retriving the DDL for the creation of external tables,
        It retrieves information of the columns and the tables
        And generate the SQL to create the table
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)
        subject.find_columns = MagicMock(return_value=dict(somevalue='value'))
        subject.table_information = MagicMock(
            return_value=dict(someother='bamm'))
        subject.execute(table_oid=14)

        subject.find_columns.assert_called_with(14)
        subject.table_information.assert_called_with(14)
        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/create.sql',
            table=dict(
                someother='bamm',
                columns=dict(somevalue='value')
            )
        )

    def test_find_columns_with_external_tables(self):
        """
        When an external table exists and have 3 columns,
        It returns a list with 1 object that as the table name to inherit from
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (True, dict(rows=[
            {
                'name': 'column_1',
                'cltype': 'text',
                'inheritedFrom': 'other_table',
                'inheritedid': '1234',
            }, {
                'name': 'column_2',
                'cltype': 'int',
                'inheritedFrom': 'other_table',
                'inheritedid': '1234',
            }, {
                'name': 'column_3',
                'cltype': 'numeric',
                'inheritedFrom': 'other_table',
                'inheritedid': '1234',
            }
        ]))

        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)

        result = subject.find_columns(table_oid=123)

        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_columns.sql',
            table_oid=123
        )

        result | should.be.equal.to([
            {
                'name': 'column_1',
                'type': 'text'
            },
            {
                'name': 'column_2',
                'type': 'int'
            },
            {
                'name': 'column_3',
                'type': 'numeric'
            },
        ])

    def test_find_columns_with_error(self):
        """
            When error happens while retrieving column information,
            It raise an exception
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (False, 'Some error message')

        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)

        (lambda: subject.find_columns(table_oid=123)) | \
            should.raises(ReverseEngineerDDLException)

        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_columns.sql',
            table_oid=123
        )

    def test_table_information_with_error(self):
        """
            When error happens while retrieving table generic information,
            It raise an exception
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (False, 'Some error message')

        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)

        (lambda: subject.table_information(table_oid=123)) | \
            should.raises(ReverseEngineerDDLException)

        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_table_information.sql',
            table_oid=123
        )

    def test_table_information_on_table_not_found(self):
        """
            When cannot find table
            It raise an exception
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (True, {'rows': []})

        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)

        (lambda: subject.table_information(table_oid=123)) | \
            should.raises(ReverseEngineerDDLException)

        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_table_information.sql',
            table_oid=123
        )

    def test_table_information(self):
        """
             When retrieving generic information about a Web table,
             It returns the table information
        """
        render_template_mock = MagicMock()
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (True, dict(rows=[
            {
                'urilocation': '{http://someurl.com}',
                'execlocation': ['ALL_SEGMENTS'],
                'fmttype': 'a',
                'fmtopts': 'delimiter \',\' null \'\' '
                           'escape \'"\' quote \'"\'',
                'command': None,
                'rejectlimit': None,
                'rejectlimittype': None,
                'errtblname': None,
                'errortofile': None,
                'pg_encoding_to_char': 'UTF8',
                'writable': False,
                'options': None,
                'distribution': None,
                'name': 'some_table',
                'namespace': 'public'
            }
        ]))

        subject = ReverseEngineerDDL(
            'sql/#gpdb#80323#/',
            render_template_mock,
            connection,
            1, 2, 3)

        subject.table_information(table_oid=123) | should.be.equal.to(
            {
                'uris': ['http://someurl.com'],
                'isWeb': True,
                'executionLocation': dict(type='all_segments', value=None),
                'formatType': 'avro',
                'formatOptions': 'delimiter = $$,$$,escape = $$"$$,'
                                 'null = $$$$,quote = $$"$$',
                'command': None,
                'rejectLimit': None,
                'rejectLimitType': None,
                'errorTableName': None,
                'erroToFile': None,
                'pgEncodingToChar': 'UTF8',
                'writable': False,
                'options': None,
                'distribution': None,
                'name': 'some_table',
                'namespace': 'public'
            })

        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_table_information.sql',
            table_oid=123

        )
