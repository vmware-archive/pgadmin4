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
    .external_tables import Properties
from pgadmin.browser.server_groups.servers.databases.external_tables \
    .properties import PropertiesException

if sys.version_info < (3, 3):
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


class TestProperties(object):

    def test_properties_existing_table(self):
        """
        When retrieving properties on an existing external table
        It returns the properties
        """
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (True, dict(
            rows=[dict(
                urilocation='{http://someurl.com}',
                execlocation=['ALL_SEGMENTS'],
                fmttype='a',
                fmtopts='delimiter \',\' null \'\' '
                        'escape \'"\' quote \'"\'',
                command=None,
                rejectlimit=None,
                rejectlimittype=None,
                errtblname=None,
                errortofile=None,
                pg_encoding_to_char='UTF8',
                writable=False,
                options=None,
                distribution=None,
                name='some_table',
                namespace='public'
            )]
        ))

        render_template_mock = MagicMock()
        external_tables_view = Properties(
            render_template_mock,
            connection,
            'some/sql/location/'
        )
        result = external_tables_view.retrieve(table_oid=11)

        render_template_mock.assert_called_with(
            template_name_or_list='some/sql/location/'
                                  'get_table_information.sql',
            table_oid=11
        )

        result | should.be.equal.to(
            dict(
                name="some_table",
                type='readable',
                format_type='UTF8',
                format_options='delimiter \',\' null \'\' '
                               'escape \'"\' quote \'"\'',
                external_options=None,
                command=None,
                execute_on='all segments',
            )
        )

    @patch('pgadmin.browser.server_groups.servers.databases'
           '.external_tables.properties.internal_server_error')
    def test_properties_database_error(self, internal_server_error_mock):
        """
        When retrieving properties of an external table
        And a SQL error happens,
        It raises exception with the error message
        """
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (False, 'Some error')
        render_template_mock = MagicMock()

        subject = Properties(
            render_template_mock,
            connection,
            'some/sql/location/'
        )

        (lambda: subject.retrieve(table_oid=11)) | \
            should.raises(PropertiesException)

        render_template_mock.assert_called_with(
            template_name_or_list='some/sql/location/'
                                  'get_table_information.sql',
            table_oid=11
        )

        internal_server_error_mock.assert_called_with(
            'Some error'
        )

    def test_properties_404_error(self):
        """
        When retrieving the properties of a external table
        And table is not found,
        It raises exception
        """
        connection = MagicMock(execute_2darray=MagicMock())
        connection.execute_2darray.return_value = (True, dict(rows=[]))
        render_template_mock = MagicMock()

        subject = Properties(
            render_template_mock,
            connection,
            'some/sql/location/'
        )

        (lambda: subject.retrieve(table_oid=11)) | \
            should.raises(PropertiesException)

        render_template_mock.assert_called_with(
            template_name_or_list='some/sql/location/'
                                  'get_table_information.sql',
            table_oid=11
        )
