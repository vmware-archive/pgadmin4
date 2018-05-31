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

from pgadmin.browser.server_groups.servers.databases.external_tables import \
    ExternalTablesView
from pgadmin.utils.base_test_generator import BaseTestGenerator

if sys.version_info < (3, 3):
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


class TestExternalTablesView(BaseTestGenerator):
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_precondition(self, _, get_driver_mock):
        """When an HTTP request is made
        it stores the manager and connection in the class object"""
        manager = MagicMock()
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(rows=[])))
        )
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.nodes(server_group_id=0,
                                   server_id=1,
                                   database_id=2)

        manager.connection.assert_called_with(did=2)
        manager | should.be.equal.to(external_tables_view.manager)
        manager.connection | should.be.equal \
            .to(external_tables_view.connection)

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_json_response')
    def test_children(self, make_json_response_mock):
        """
        When retrieving the tree node underneath external tables
        It returns empty children list and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(rows=[])))
        )
        manager.connection = MagicMock(return_value=return_value)

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.children(server_group_id=0,
                                      server_id=1,
                                      database_id=2)
        make_json_response_mock.assert_called_with(
            data=[]
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_json_response')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_nodes_without_children(self,
                                    render_template_mock,
                                    make_json_response_mock,
                                    get_driver_mock):
        """
        When retrieving the tree nodes
        And the database has no external tables
        It returns empty tree node list and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(rows=[])))
        )
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.nodes(server_group_id=0,
                                   server_id=1,
                                   database_id=2)

        make_json_response_mock.assert_called_with(data=[],
                                                   status=200)
        render_template_mock.assert_called_with(
            'sql/#gpdb#80323#/list.sql'
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.internal_server_error')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_error_retrieving_nodes(self,
                                    render_template_mock,
                                    internal_server_error_mock,
                                    get_driver_mock):
        """
        When retrieving the tree nodes
        And the database has no external tables
        It returns empty tree node list and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(False, 'Some error message')
        ))
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.nodes(server_group_id=0,
                                   server_id=1,
                                   database_id=2)

        internal_server_error_mock.assert_called_with(
            errormsg='Some error message'
        )
        render_template_mock.assert_called_with(
            'sql/#gpdb#80323#/list.sql'
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_json_response')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_nodes_with_2_external_tables(self,
                                          render_template_mock,
                                          make_json_response_mock,
                                          get_driver_mock):
        """
        When retrieving the tree nodes
        And the database has 2 external tables
        It returns tree node list with 2 child nodes
        and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(
                rows=[
                    dict(
                        oid='oid1',
                        name='table_one'
                    ),
                    dict(
                        oid='oid2',
                        name='table_two'
                    ),
                ]
            )))
        )
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.nodes(server_group_id=0,
                                   server_id=1,
                                   database_id=2)

        make_json_response_mock.assert_called_with(
            data=[
                {
                    'id': "external_table/oid1",
                    'label': 'table_one',
                    'icon': 'icon-external_table',
                    'inode': False,
                    '_type': 'external_table',
                    '_id': 'oid1',
                    '_pid': 2,
                    'module': 'pgadmin.node.external_table'
                },
                {
                    'id': "external_table/oid2",
                    'label': 'table_two',
                    'icon': 'icon-external_table',
                    'inode': False,
                    '_type': 'external_table',
                    '_id': 'oid2',
                    '_pid': 2,
                    'module': 'pgadmin.node.external_table'
                }
            ], status=200)
        render_template_mock.assert_called_with(
            'sql/#gpdb#80323#/list.sql'
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.internal_server_error')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_error_retrieving_node_with_1_external_table(
        self,
        render_template_mock,
        internal_server_error_mock,
        get_driver_mock
    ):
        """
        When retrieving the tree nodes
        And the database has 1 external tables
        And it errors executing the query
        It returns an internal server error
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(False, 'Some error message')
        ))
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.node(server_group_id=0,
                                  server_id=1,
                                  database_id=2,
                                  external_table_id=11)

        internal_server_error_mock.assert_called_with(
            errormsg='Some error message'
        )
        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/node.sql',
            external_table_id=11
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_json_response')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_error_retrieving_nonexistent_node_with_1_external_table(
        self,
        render_template_mock,
        make_json_response_mock,
        get_driver_mock
    ):
        """
        When retrieving the tree nodes
        And the database has 1 external tables
        And it errors executing the query
        It returns a 404 error
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(rows=[]))
        ))
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.node(server_group_id=0,
                                  server_id=1,
                                  database_id=2,
                                  external_table_id=11)

        make_json_response_mock.assert_called_with(
            data='Could not find the external table.',
            status=404
        )
        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/node.sql',
            external_table_id=11
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_json_response')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_node_with_1_external_tables(self,
                                         render_template_mock,
                                         make_json_response_mock,
                                         get_driver_mock):
        """
        When retrieving the tree nodes
        And the database has 1 external tables
        It returns tree node
        and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(
                rows=[
                    dict(
                        oid='oid1',
                        name='table_one'
                    ),
                    dict(
                        oid='oid2',
                        name='table_two'
                    ),
                ]
            )))
        )
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.node(server_group_id=0,
                                  server_id=1,
                                  database_id=2,
                                  external_table_id=11)

        make_json_response_mock.assert_called_with(
            data={
                'id': "external_table/oid1",
                'label': 'table_one',
                'icon': 'icon-external_table',
                'inode': False,
                '_type': 'external_table',
                '_id': 'oid1',
                '_pid': 2,
                'module': 'pgadmin.node.external_table'
            },
            status=200
        )
        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/node.sql',
            external_table_id=11
        )

    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.get_driver')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.make_response')
    @patch('pgadmin.browser.server_groups.servers.databases.external_tables'
           '.render_template')
    def test_properties_with_1_external_tables(self,
                                               render_template_mock,
                                               make_response_mock,
                                               get_driver_mock):
        """
        When retrieving the properties of 1 external table
        It returns properties of the tree node
        and status of 200
        """
        manager = MagicMock(server_type='gpdb', sversion=80323)
        return_value = MagicMock(execute_2darray=MagicMock(
            return_value=(True, dict(
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
            )))
        )
        manager.connection = MagicMock(return_value=return_value)

        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(return_value=manager)
        )

        external_tables_view = ExternalTablesView(cmd='')
        external_tables_view.properties(server_group_id=0,
                                        server_id=1,
                                        database_id=2,
                                        external_table_id=11)

        make_response_mock.assert_called_with(
            response=dict(
                name="some_table",
                type='readable',
                format_type='UTF8',
                format_options='delimiter \',\' null \'\' '
                               'escape \'"\' quote \'"\'',
                external_options=None,
                command=None,
                execute_on='all segments',
            ),
            status=200
        )
        render_template_mock.assert_called_with(
            template_name_or_list='sql/#gpdb#80323#/get_table_information.sql',
            table_oid=11
        )
