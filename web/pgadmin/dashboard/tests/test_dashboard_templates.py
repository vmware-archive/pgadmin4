##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os
import sys
from flask import Flask, render_template
from grappa import should
from jinja2 import FileSystemLoader
from pgadmin import VersionedTemplateLoader
from pgadmin.utils.base_test_generator import BaseTestGenerator

if sys.version_info < (3, 3):
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

# Hard coded dummy input parameters for the templates
RATES = {
    'session_stats_refresh': 1,
    'tps_stats_refresh': 1,
    'ti_stats_refresh': 1,
    'to_stats_refresh': 1,
    'bio_stats_refresh': 1
}

DISPLAY_DASHBOARD = {
    'both': {
        'show_graphs': True,
        'show_activity': True
    },

    'only_graphs': {
        'show_graphs': True,
        'show_activity': False
    },

    'only_server_activity': {
        'show_graphs': False,
        'show_activity': True
    },

    'none': {
        'show_graphs': False,
        'show_activity': False
    }
}

VERSION = 95000

SERVER_ID = 1

DATABASE_ID = 123


# To moke gettext function used in the template
_ = MagicMock(side_effect=lambda x: x)


class TestDashboardTemplates:
    def testDashboardTemplGraphsAndServer(self):
        """
        Dashboard should be able to render html page with graphs
        and server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/server_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['both'],
                _=_
            )

            result | should.contain("Server sessions")
            result | should.contain("Server activity")

    def testDashboardTemplGraphs(self):
        """
        Dashboard should be able to render html page
        with only graph related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/server_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['only_graphs'],
                _=_
            )

            result | should.contain("Server sessions")
            result | should._not.contain("Server activity")

    def testDashboardTemplServer(self):
        """
        Dashboard should be able to render html page
        with only server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/server_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['only_server_activity'],
                _=_
            )

            result | should.contain("Server activity")
            result | should._not.contain("Server sessions")

    def testDashboardTemplNone(self):
        """
        Dashboard should be able to render html page
        with only server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/server_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['none'],
                _=_
            )

            result | should._not.contain("Server activity")
            result | should._not.contain("Server sessions")

    def testDBDashboardTemplGraphsAndServer(self):
        """
        DB Dashboard should be able to render html page with graphs
        and server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/database_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['both'],
                _=_
            )

            result | should.contain("Database sessions")
            result | should.contain("Database activity")

    def testDBDashboardTemplGraphs(self):
        """
        DB Dashboard should be able to render html page
        with only graph related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/database_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['only_graphs'],
                _=_
            )

            result | should.contain("Database sessions")
            result | should._not.contain("Database activity")

    def testDBDashboardTemplServer(self):
        """
        DB Dashboard should be able to render html page
        with only server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/database_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['only_server_activity'],
                _=_
            )

            result | should.contain("Database activity")
            result | should._not.contain("Database sessions")

    def testDBDashboardTemplNone(self):
        """
        DB Dashboard should be able to render html page
        with only server activity related elements
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'dashboard/database_dashboard.html',
                sid=SERVER_ID,
                did=None,
                rates=RATES,
                version=VERSION,
                settings=DISPLAY_DASHBOARD['none'],
                _=_
            )

            result | should._not.contain("Database activity")
            result | should._not.contain("Database sessions")


class FakeApp(Flask):
    def __init__(self):
        super(FakeApp, self).__init__("")
        self.jinja_loader = FileSystemLoader(
            os.path.dirname(os.path.realpath(__file__)) + "/../templates"
        )
