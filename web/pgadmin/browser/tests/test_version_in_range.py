##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should

from pgadmin.browser.utils import is_version_in_range


class TestVersionInRange(object):
    def test_version_in_range_pg8_23(self):
        """
        When Validating pgversion 8.23
        And the min_version is 91000
        It should return false
        """

        result = is_version_in_range(
            82300,
            90100,
            1000000000
        )

        result | should.be.false

    def test_version_in_range_pg9_2(self):
        """
        When Validating pgversion 9.2
        It should return true
        """

        result = is_version_in_range(
            90200,
            0,
            1000000000,
        )

        result | should.be.true

    def test_version_in_range_pg9_none(self):
        """
        When Validating pgversion 9.2
        And the min/max are None
        It should return true
        """

        result = is_version_in_range(
            90200,
            None,
            None,
        )

        result | should.be.true

    def test_version_in_range_pg9_6_lower_max(self):
        """
        When Validating pgversion 9.6
        And the max is lower
        It should return false
        """

        result = is_version_in_range(
            90600,
            None,
            90400,
        )

        result | should.be.false
