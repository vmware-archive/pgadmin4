##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os

import pytest
from flask import Flask
from grappa import should
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound

from pgadmin import VersionedTemplateLoader
from pgadmin.utils.base_test_generator import BaseTestGenerator


class TestVersionedTemplateLoader(BaseTestGenerator):
    """Test Versioned template loader"""

    @pytest.fixture(autouse=True)
    def setup_tests(self):
        setattr(self, 'setup_not_needed', True)
        self.loader = VersionedTemplateLoader(FakeApp())

    def test_get_source_returns_a_template(self):
        """Render a template when called"""
        expected_content = "Some SQL" \
                           "\nsome more stuff on a new line\n"
        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join(
            "some_feature", "sql", "9.1_plus", "some_action.sql"
        )
        content, filename, up_to_dateness = self.loader.get_source(
            None, "some_feature/sql/9.1_plus/some_action.sql"
        )
        expected_content | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_get_source_when_the_version_is_9_1(self):
        """Render a version 9.1 template when it is present"""
        expected_content = "Some SQL" \
                           "\nsome more stuff on a new line\n"
        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join(
            "some_feature", "sql", "9.1_plus", "some_action.sql"
        )
        content, filename, up_to_dateness = self.loader.get_source(
            None, "some_feature/sql/#90100#/some_action.sql"
        )

        expected_content | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_get_source_when_the_version_is_9_3(self):
        """Render a version 9.2 template when request for a higher version"""
        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join(
            "some_feature", "sql", "9.2_plus", "some_action.sql"
        )
        content, filename, up_to_dateness = self.loader.get_source(
            None, "some_feature/sql/#90300#/some_action.sql"
        )

        "Some 9.2 SQL" | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_get_source_when_the_version_is_9_0(self):
        """Render default version when version 9.0 was requested and only
        9.1 and 9.2 are present"""

        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join("some_feature", "sql",
                                "default", "some_action_with_default.sql")
        content, filename, up_to_dateness = self.loader.get_source(
            None,
            "some_feature/sql/#90000#/some_action_with_default.sql")

        "Some default SQL" | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_raise_not_found_exception(self):
        """Raise error when version is smaller than available templates"""
        (lambda: self.loader.get_source(
            None, "some_feature/sql/#10100#/some_action.sql"
        )) | should.raises(TemplateNotFound)

    def test_get_source_when_the_version_is_gpdb_5_0(self):
        """Render a version GPDB 5.0 template when it is present"""
        expected_content = "Some default SQL for GPDB\n"
        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join(
            "some_feature", "sql", "gpdb_5.0_plus",
            "some_action_with_gpdb_5_0.sql"
        )
        content, filename, up_to_dateness = self.loader.get_source(
            None,
            "some_feature/sql/#gpdb#80323#/some_action_with_gpdb_5_0.sql"
        )

        expected_content | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_get_source_when_the_version_is_gpdb_5_0_returns_default(self):
        """Render a version GPDB 5.0 template when it is in default"""
        expected_content = "Some default SQL"
        # For cross platform we join the SQL path
        # (This solves the slashes issue)
        sql_path = os.path.join(
            "some_feature", "sql", "default", "some_action_with_default.sql"
        )
        content, filename, up_to_dateness = self.loader.get_source(
            None, "some_feature/sql/#gpdb#80323#/some_action_with_default.sql"
        )

        expected_content | should.be.equal.to(str(content).replace("\r", ""))

        filename | should.contain.item(sql_path)

    def test_raise_not_found_exception_when_the_version_is_gpdb(self):
        """"Raise error when version is gpdb but template does not exist"""
        (lambda: self.loader.get_source(
            None, "some_feature/sql/#gpdb#50100#/some_action.sql"
        )) | should.raises(TemplateNotFound)


class FakeApp(Flask):
    def __init__(self):
        super(FakeApp, self).__init__("")
        self.jinja_loader = FileSystemLoader(
            os.path.dirname(os.path.realpath(__file__)) + "/templates"
        )
