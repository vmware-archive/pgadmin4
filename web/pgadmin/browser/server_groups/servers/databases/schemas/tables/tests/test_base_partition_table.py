##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas \
    .tables.base_partition_table import BasePartitionTable


class TestIsTablePartitioned:
    """
    test #is_table_partitioned
    """
    @pytest.mark.parametrize(
        'input_parameters, expected_return, node_type', [
            (dict(), False, None),
            (dict(is_partitioned=True), True, None),
            (dict(is_partitioned=False), False, None),
            (dict(is_partitioned=False), True, 'partition'),
            (dict(is_partitioned=False), False, 'table'),
        ])
    def test_is_table_partitioned(self,
                                  input_parameters,
                                  expected_return,
                                  node_type):
        subject = BasePartitionTable()
        if node_type is not None:
            subject.node_type = node_type

        subject.is_table_partitioned(input_parameters) | should.be.equal.to(
            expected_return)


class TestGetIconCSSClass:
    """
    test #get_icon_css_class
    """
    @pytest.mark.parametrize(
        'input_parameters, expected_return', [
            (dict(is_partitioned=True), 'icon-partition'),
            (dict(is_partitioned=False), 'icon-table'),
        ])
    def test_get_icon_css_class(self, input_parameters, expected_return):
        subject = BasePartitionTable()

        subject.get_icon_css_class(input_parameters) | should.be.equal.to(
            expected_return)
