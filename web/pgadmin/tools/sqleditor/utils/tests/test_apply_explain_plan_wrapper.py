#######################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import sys

from grappa import should

from pgadmin.tools.sqleditor.utils import apply_explain_plan_wrapper_if_needed

if sys.version_info < (3, 3):
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock


class TestStartRunningQuery:
    @patch('pgadmin.tools.sqleditor.utils.apply_explain_plan_wrapper'
           '.render_template')
    def testStartRunningQueryNoExplainPlan1(self, render_template_mock):
        """
        When the StartRunningQueryTest method is invoked
        And the explain plan is not present
        It returns unaltered SQL
        """
        result = apply_explain_plan_wrapper_if_needed(
            MagicMock(), {
                'sql': 'some sql',
                'explain_plan': None
            }
        )

        result | should.be.equal.to('some sql')
        render_template_mock.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.apply_explain_plan_wrapper'
           '.render_template')
    def testStartRunningQueryNoExplainPlan2(self, render_template_mock):
        """
        When the StartRunningQueryTest method is invoked
        And the explain plan is not present
        It returns unaltered SQL
        """
        result = apply_explain_plan_wrapper_if_needed(
            MagicMock(), {
                'sql': 'some sql',
            }
        )

        result | should.be.equal.to('some sql')
        render_template_mock.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.apply_explain_plan_wrapper'
           '.render_template')
    def testStartRunningQueryPgExplainPlan(self, render_template_mock):
        """
        When the StartRunningQueryTest method is invoked
        And the explain plan is present for postgres
        It returns SQL with the explain plan
        """

        expected_return_value = 'EXPLAIN (FORMAT JSON, ANALYZE FALSE, ' \
                                'VERBOSE TRUE, COSTS FALSE, BUFFERS FALSE, ' \
                                'TIMING TRUE) some sql'

        render_template_mock.return_value = expected_return_value

        result = apply_explain_plan_wrapper_if_needed(
            MagicMock(version=10, server_type='pg'), {
                'sql': 'some sql',
                'explain_plan': {
                    'format': 'json',
                    'analyze': False,
                    'verbose': True,
                    'buffers': False,
                    'timing': True
                }
            }
        )

        result | should.be.equal.to(expected_return_value)
        render_template_mock.assert_called_with(
            'sqleditor/sql/#10#/explain_plan.sql',
            format='json',
            analyze=False,
            verbose=True,
            buffers=False,
            timing=True,
            sql='some sql'
        )

    @patch('pgadmin.tools.sqleditor.utils.apply_explain_plan_wrapper'
           '.render_template')
    def testStartRunningQueryGpdbExplainPlan(self, render_template_mock):
        """
        When the StartRunningQueryTest method is invoked
        And the explain plan is present for GPDB
        It returns SQL with the explain plan
        """

        expected_return_value = 'EXPLAIN (FORMAT JSON, ANALYZE FALSE, ' \
                                'VERBOSE TRUE, COSTS FALSE, BUFFERS FALSE, ' \
                                'TIMING TRUE) some sql'

        render_template_mock.return_value = expected_return_value

        result = apply_explain_plan_wrapper_if_needed(
            MagicMock(version=80323, server_type='gpdb'), {
                'sql': 'some sql',
                'explain_plan': {
                    'format': 'json',
                    'analyze': False,
                    'verbose': True,
                    'buffers': False,
                    'timing': True
                }
            }
        )

        result | should.be.equal.to(expected_return_value)
        render_template_mock.assert_called_with(
            'sqleditor/sql/#gpdb#80323#/explain_plan.sql',
            format='json',
            analyze=False,
            verbose=True,
            buffers=False,
            timing=True,
            sql='some sql'
        )
