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

from pgadmin.browser.server_groups.servers.databases.schemas.tables import \
    BaseTableView
from pgadmin.utils.base_test_generator import BaseTestGenerator

if sys.version_info < (3, 3):
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


class BaseView(BaseTableView):
    @BaseTableView.check_precondition
    def test(self, did, sid):
        pass


class TestUtils(BaseTestGenerator):
    @patch('pgadmin.browser.server_groups.servers'
           '.databases.schemas.tables.utils'
           '.get_driver')
    def test_wrapping_function(self, get_driver_mock):
        """
        It returns stubbed values for tests
        """

        subject = BaseView(cmd='something')
        get_driver_mock.return_value = MagicMock(
            connection_manager=MagicMock(
                return_value=MagicMock(
                    connection=MagicMock(),
                    db_info={
                        1: dict(datlastsysoid=False)
                    },
                    version=10,
                    server_type='gpdb'
                )
            ),
            qtIndent=MagicMock(),
            qtTypeIdent=MagicMock()
        )

        subject.test(did=1, sid=2)

        subject.table_template_path | \
            should.equal('table/sql/#gpdb#10#')
        subject.data_type_template_path | \
            should.equal('datatype/sql/#gpdb#10#')
        subject.check_constraint_template_path | \
            should.equal('check_constraint/sql/#gpdb#10#')
        subject.exclusion_constraint_template_path | \
            should.equal('exclusion_constraint/sql/#gpdb#10#')
        subject.foreign_key_template_path | \
            should.equal('foreign_key/sql/#gpdb#10#')
        subject.index_template_path | \
            should.equal('index/sql/#gpdb#10#')
        subject.trigger_template_path | \
            should.equal('trigger/sql/#gpdb#10#')
