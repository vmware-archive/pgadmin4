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

if sys.version_info < (3, 3):
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

from pgadmin.browser.server_groups.servers.tablespaces import TablespaceModule


class TestBackendSupported:
    def test_postgres(self):
        """
        When checking if the Postgres Database supports Table spaces
        It returns true
        """
        module = TablespaceModule('name')
        manager = MagicMock()
        manager.sversion = 90100
        manager.server_type = 'pg'
        module.BackendSupported(manager) | should.be.true

    def test_greenplum(self):
        """
        When checking if the Greenplum Database supports Tablespaces
        It returns false
        """
        module = TablespaceModule('name')
        manager = MagicMock()
        manager.sversion = 80323
        manager.server_type = 'gpdb'
        module.BackendSupported(manager) | should.be.false
