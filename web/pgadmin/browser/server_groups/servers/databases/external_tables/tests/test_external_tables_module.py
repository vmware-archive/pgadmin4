##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import sys

import six
from grappa import should

from pgadmin.browser.server_groups.servers \
    .databases.external_tables import ExternalTablesModule

if sys.version_info < (3, 3):
    from mock import MagicMock, Mock
else:
    from unittest.mock import MagicMock, Mock


class TestExternalTablesModule(object):
    def test_backend_support_on_postgresql(self):
        """When accessed on Postgresql Database"""
        manager = MagicMock()
        manager.sversion = 90100
        manager.server_type = 'pg'
        module = ExternalTablesModule('something')
        module.BackendSupported(manager) | should.be.false

    def test_backend_support_greenplum(self):
        """When accessed on GreenPlum Database"""
        manager = MagicMock()
        manager.sversion = 82303
        manager.server_type = 'gpdb'
        module = ExternalTablesModule('something')
        module.BackendSupported(manager) | should.be.true

    def test_get_nodes(self):
        """when trying to retrieve the node,
         it calls the generate_browser_collection_node function
        with value 12"""
        module = ExternalTablesModule('something')
        module.generate_browser_collection_node = Mock()

        result = module.get_nodes(gid=10,
                                  sid=11,
                                  did=12)
        six.next(result)

        module.generate_browser_collection_node.assert_called_with(12)

    def test_template_javascript(self):
        """when checking if it needs to generate javascript from template,
        it should return false"""
        module = ExternalTablesModule('something')
        module.module_use_template_javascript | should.be.false
