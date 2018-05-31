##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should

from pgadmin.tools.sqleditor.utils.query_tool_preferences import \
    get_text_representation_of_shortcut


class TestQueryToolPreference:
    def test_shortcut_a(self):
        """
        When the the shortcut pressed is 'a'
        It return the string 'a'
        """
        result = get_text_representation_of_shortcut(
            dict(
                alt=False,
                shift=False,
                control=False,
                key=dict(
                    char='a',
                    keyCode=65
                )
            ))
        result | should.be.equal('a')

    def test_shortcut_alt_a(self):
        """
        When the the shortcut pressed is ALT + 'a'
        It return the string 'Alt+a'
        """
        result = get_text_representation_of_shortcut(
            dict(
                alt=True,
                shift=False,
                control=False,
                key=dict(
                    char='a',
                    keyCode=65
                )
            ))
        result | should.be.equal('Alt+a')

    def test_shortcut_alt_shit_control_a(self):
        """
        When the the shortcut pressed is Alt + Control + Shift + 'a'
        It return the string 'Alt+Shift+Ctrl+a'
        """
        result = get_text_representation_of_shortcut(
            dict(
                alt=True,
                shift=True,
                control=True,
                key=dict(
                    char='a',
                    keyCode=65
                )
            ))
        result | should.be.equal('Alt+Shift+Ctrl+a')

    def test_shortcut_shit_a(self):
        """
        When the the shortcut pressed is Shift + 'a'
        It return the string 'Shift+a'
        """
        result = get_text_representation_of_shortcut(
            dict(
                alt=False,
                shift=True,
                control=False,
                key=dict(
                    char='a',
                    keyCode=65
                )
            ))
        result | should.be.equal('Shift+a')

    def test_shortcut_alt_shit_a(self):
        """
        When the the shortcut pressed is Alt + Shift + 'a'
        It return the string 'Alt+Shift+a'
        """
        result = get_text_representation_of_shortcut(dict(
            alt=True,
            shift=True,
            control=False,
            key=dict(
                char='a',
                keyCode=65
            )
        ))
        result | should.be.equal('Alt+Shift+a')

    def test_shortcut_invalid(self):
        """
        When the function receives None as the shortcut
        It return empty string
        """
        result = get_text_representation_of_shortcut(None)
        result | should.be.equal('')
