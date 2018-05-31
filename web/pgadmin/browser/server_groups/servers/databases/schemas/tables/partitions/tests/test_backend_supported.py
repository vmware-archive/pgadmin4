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

from pgadmin.browser.server_groups.servers.databases.schemas.tables. \
    partitions import PartitionsModule

if sys.version_info < (3, 3):
    from mock import patch, Mock, call
else:
    from unittest.mock import patch, Mock, call


class TestBackendSupport:
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.CollectionNodeModule'
    )
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.render_template'
    )
    def test_not_all_arguments_present(
        self, render_template_mock, CollectionNodeModule_mock
    ):
        """
        When tid is not present in the arguments
        It return None and no query should be done
        """
        module = PartitionsModule('partition')
        module.manager = Mock()
        module.manager.server_type = ''
        module.manager.version = ''
        connection_mock = Mock()
        connection_mock.execute_scalar.return_value = []
        module.manager.connection.return_value = connection_mock
        CollectionNodeModule_mock.BackendSupported.return_value = True

        result = module.BackendSupported(
            module.manager,
            did=432
        )

        render_template_mock.assert_not_called()

        result | should.be.none

    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.CollectionNodeModule'
    )
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.render_template'
    )
    def test_tid_present_not_supported(
        self, render_template_mock, CollectionNodeModule_mock
    ):
        """
        when tid is present in arguments
        And CollectionNodeModule does not support
        It return None and no query should be done
        """
        module = PartitionsModule('partition')
        module.manager = Mock()
        module.manager.server_type = ''
        module.manager.version = ''
        connection_mock = Mock()
        connection_mock.execute_scalar.return_value = []
        module.manager.connection.return_value = connection_mock
        CollectionNodeModule_mock.BackendSupported.return_value = False

        result = module.BackendSupported(
            module.manager,
            did=432,
            tid=123
        )

        render_template_mock.assert_not_called()

        result | should.be.none

    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.CollectionNodeModule'
    )
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.render_template'
    )
    def test_table_partitioned(
        self, render_template_mock, CollectionNodeModule_mock
    ):
        """
        When table is partitioned
        It return the table identifier
        """
        module = PartitionsModule('partition')
        module.manager = Mock()
        module.manager.server_type = 'gpdb'
        module.manager.version = '5'
        connection_mock = Mock()
        connection_mock.execute_scalar.return_value = [True, 123]
        module.manager.connection.return_value = connection_mock
        CollectionNodeModule_mock.BackendSupported.return_value = True

        result = module.BackendSupported(
            module.manager,
            did=432,
            tid=123
        )

        render_template_mock.assert_has_calls(
            [call('partition/sql/gpdb/#gpdb#5#/backend_support.sql', tid=123)]
        )

        result | should.be.equal.to(123)

    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.internal_server_error'
    )
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.CollectionNodeModule'
    )
    @patch(
        'pgadmin.browser.server_groups.servers.databases.schemas.tables.'
        'partitions.render_template'
    )
    def test_error_while_querying_database(
        self, render_template_mock, CollectionNodeModule_mock,
        internal_server_error_mock
    ):
        """
        When error happens while querying the database
        It return an internal server error
        """
        module = PartitionsModule('partition')
        module.manager = Mock()
        module.manager.server_type = 'pg'
        module.manager.version = '10'
        connection_mock = Mock()
        connection_mock.execute_scalar.return_value = [
            False,
            'Some ugly error']
        module.manager.connection.return_value = connection_mock
        CollectionNodeModule_mock.BackendSupported.return_value = True

        module.BackendSupported(
            module.manager,
            did=432,
            tid=123
        )

        render_template_mock.assert_has_calls(
            [call('partition/sql/pg/#pg#10#/backend_support.sql', tid=123)]
        )

        internal_server_error_mock.assert_called_with(
            errormsg='Some ugly error'
        )
