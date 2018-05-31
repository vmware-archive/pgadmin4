##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os
import re

from flask import Flask, render_template
from grappa import should
from jinja2 import FileSystemLoader, ChoiceLoader

from config import PG_DEFAULT_DRIVER
from pgadmin import VersionedTemplateLoader
from pgadmin.utils.driver import get_driver


class TestTemplateCreate:
    def test_template_create(self):
        """
        When rendering GreenPlum 5.3 template
        when no distribution is present
        when no primary key is present
        it returns "DISTRIBUTED RANDOMLY"
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'table/sql/gpdb_5.0_plus/create.sql',
                data=dict()
            )
            result_beautified = re.sub(
                ' +', ' ', str(result).replace("\n", " ").strip())

            result_beautified | should.contain('DISTRIBUTED RANDOMLY')
            result_beautified | should.to_not.contain(
                'DISTRIBUTED BY '
            )

    def test_template_create_primary_key(self):
        """
        When rendering GreenPlum 5.3 template
        when no distribution is present
        when primary key is present
        it returns "DISTRIBUTED BY (attr_primary_key)"
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'table/sql/gpdb_5.0_plus/create.sql',
                data=dict(
                    primary_key=[
                        dict(
                            columns=[dict(
                                column='attr_primary_key_column_1'
                            ), dict(
                                column='attr_primary_key_column_2'
                            )]
                        )
                    ]
                )
            )
            result_beautified = re.sub(
                ' +', ' ', str(result).replace("\n", " ").strip())

            result_beautified | should.contain('DISTRIBUTED BY '
                                               '(attr_primary_key_column_1, '
                                               'attr_primary_key_column_2)')
            result_beautified | should.to_not.contain(
                'DISTRIBUTED RANDOMLY'
            )

    def test_template_create_distribution(self):
        """
        When rendering GreenPlum 5.3 template
        when distribution is present
        it returns "DISTRIBUTED BY (attr1, attr2, attr4)"
        """

        self.loader = VersionedTemplateLoader(FakeApp())

        with FakeApp().app_context():
            result = render_template(
                'table/sql/gpdb_5.0_plus/create.sql',
                data=dict(
                    distribution=[1, 2, 4],
                    columns=[
                        {'name': 'attr1'},
                        {'name': 'attr2'},
                        {'name': 'attr3'},
                        {'name': 'attr4'},
                        {'name': 'attr5'},
                    ]
                )
            )
            result_beautified = re.sub(
                ' +', ' ', str(result).replace("\n", " ").strip())

            result_beautified | should.contain('DISTRIBUTED BY '
                                               '(attr1, attr2, attr4)')
            result_beautified | should.to_not.contain(
                'DISTRIBUTED RANDOMLY'
            )


class FakeApp(Flask):
    def __init__(self):
        super(FakeApp, self).__init__('')
        driver = get_driver(PG_DEFAULT_DRIVER, self)
        self.jinja_env.filters['qtLiteral'] = driver.qtLiteral
        self.jinja_env.filters['qtIdent'] = driver.qtIdent
        self.jinja_env.filters['qtTypeIdent'] = driver.qtTypeIdent
        self.jinja_loader = ChoiceLoader([
            FileSystemLoader(
                os.path.join(os.path.dirname(
                    os.path.realpath(__file__)
                ), os.pardir, 'templates')
            ),
            FileSystemLoader(
                os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)
                    ), os.pardir, os.pardir, 'templates')
            ),
            FileSystemLoader(
                os.path.join(os.path.dirname(
                    os.path.realpath(__file__)),
                    os.pardir, os.pardir, 'types', 'templates')
            ),
            FileSystemLoader(
                os.path.join(os.path.dirname(
                    os.path.realpath(__file__)),
                    os.pardir, os.pardir, os.pardir, os.pardir,
                    'templates')
            ),
        ]
        )
