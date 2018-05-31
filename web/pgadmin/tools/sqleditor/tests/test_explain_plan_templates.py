##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os

from flask import Flask, render_template
from grappa import should
from jinja2 import FileSystemLoader


class TestExplainPlanTemplates:
    def test_all_parameters_on_pg_9_0(self):
        """
        When rendering Postgres 9.0 template
        when passing all parameters
        it returns the explain plan with all parameters
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/default/explain_plan.sql',
                sql='SELECT * FROM places',
                format='xml',
                analyze=True,
                verbose=True,
                costs=False,
                buffers=True)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN '
                '(FORMAT XML,ANALYZE True,'
                'VERBOSE True,COSTS False,'
                'BUFFERS True) SELECT * FROM places')

    def test_not_all_parameters_on_pg_9_0(self):
        """
        When rendering Postgres 9.0 template
        When not all parameters are present
        It returns the explain plan with the present parameters
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/default/explain_plan.sql',
                sql='SELECT * FROM places',
                format='json',
                buffers=True)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN '
                '(FORMAT JSON,BUFFERS True) '
                'SELECT * FROM places')

    def test_timing_present_on_pg_9_2(self):
        """
        When rendering Postgres 9.2 template
        When timing is present
        It returns the explain plan with timing
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/9.2_plus/explain_plan.sql',
                sql='SELECT * FROM places',
                format='json',
                buffers=True,
                timing=False)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN '
                '(FORMAT JSON,TIMING False,'
                'BUFFERS True) SELECT * FROM places')

    def test_summary_present_on_pg_10(self):
        """
        When rendering Postgres 9.2 template
        When timing is present
        It returns the explain plan with summary
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/10_plus/explain_plan.sql',
                sql='SELECT * FROM places',
                format='yaml',
                buffers=True,
                timing=False,
                summary=True)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN '
                '(FORMAT YAML,TIMING False,'
                'SUMMARY True,BUFFERS True) '
                'SELECT * FROM places')

    def test_all_parameters_present_on_gpdb_5_3(self):
        """
        When rendering GreenPlum 5.3 template
        When all parameters are present
        It returns the explain without parameters
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/gpdb_5.0_plus/explain_plan.sql',
                sql='SELECT * FROM places',
                format='json',
                buffers=True)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN SELECT * FROM places')

    def test_analyze_on_gpdb_5_3(self):
        """
        When rendering GreenPlum 5.3 template
        When analyze is true
        It returns the explain analyze
        """
        with FakeApp().app_context():
            result = render_template(
                'sqleditor/sql/gpdb_5.0_plus/explain_plan.sql',
                sql='SELECT * FROM places',
                analyze=True)

            str(result).replace("\n", "") | should.be.equal(
                'EXPLAIN ANALYZE SELECT * FROM places')


class FakeApp(Flask):
    def __init__(self):
        super(FakeApp, self).__init__("")
        self.jinja_loader = FileSystemLoader(
            os.path.dirname(os.path.realpath(__file__)) + "/../templates"
        )
