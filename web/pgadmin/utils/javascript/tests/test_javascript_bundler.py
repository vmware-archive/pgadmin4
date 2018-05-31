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

from pgadmin.utils.javascript.javascript_bundler import JavascriptBundler
from pgadmin.utils.javascript.javascript_bundler import JsState

if sys.version_info < (3, 3):
    from mock import patch
else:
    from unittest.mock import patch


class TestJavascriptBundler:

    @patch('pgadmin.utils.javascript.javascript_bundler.os')
    @patch('pgadmin.utils.javascript.javascript_bundler.call')
    def test_javascript_bundler(self, subprocessMock, osMock):
        """
        When the javascript bundler tool is run
        It causes the application to bundle
        """
        self.mockOs = osMock
        self.mockSubprocessCall = subprocessMock

        self._bundling_succeeds()
        self.reset_test_state()
        self._bundling_fails_and_there_is_no_existing_bundle()
        self.reset_test_state()
        self._bundling_fails_when_bundling_returns_nonzero()
        self.reset_test_state()
        self._bundling_fails_and_there_is_no_existing_bundle_directory()
        self.reset_test_state()
        self._bundling_fails_but_there_was_existing_bundle()
        self.reset_test_state()

    def reset_test_state(self):
        self.mockSubprocessCall.reset_mock()
        self.mockSubprocessCall.side_effect = None
        self.mockOs.reset_mock()
        self.mockOs.listdir.side_effect = None
        self.mockOs.path.exists.side_effect = None

    def _bundling_succeeds(self):
        javascript_bundler = JavascriptBundler()
        self.mockSubprocessCall.method_calls | \
            should.have.length.of(0)
        self.mockSubprocessCall.return_value = 0

        self.mockOs.listdir.return_value = [
            u'history.js', u'reactComponents.js']

        javascript_bundler.bundle()
        self.mockSubprocessCall.assert_called_once_with(
            ['yarn', 'run', 'bundle:dev'])

        self.__assertState(javascript_bundler, JsState.NEW)

    def _bundling_fails_when_bundling_returns_nonzero(self):
        javascript_bundler = JavascriptBundler()
        self.mockSubprocessCall.method_calls | \
            should.have.length.of(0)
        self.mockOs.listdir.return_value = []
        self.mockSubprocessCall.return_value = 99

        javascript_bundler.bundle()

        self.__assertState(javascript_bundler, JsState.NONE)

    def _bundling_fails_and_there_is_no_existing_bundle(self):
        javascript_bundler = JavascriptBundler()
        self.mockSubprocessCall.side_effect = OSError(
            "mock exception behavior")
        self.mockOs.path.exists.return_value = True
        self.mockOs.listdir.return_value = []

        javascript_bundler.bundle()

        self.__assertState(javascript_bundler, JsState.NONE)

    def _bundling_fails_and_there_is_no_existing_bundle_directory(self):
        javascript_bundler = JavascriptBundler()
        self.mockSubprocessCall.side_effect = OSError(
            "mock exception behavior")
        self.mockOs.path.exists.return_value = False
        self.mockOs.listdir.side_effect = OSError("mock exception behavior")

        javascript_bundler.bundle()

        self.__assertState(javascript_bundler, JsState.NONE)

    def _bundling_fails_but_there_was_existing_bundle(self):
        javascript_bundler = JavascriptBundler()
        self.mockSubprocessCall.side_effect = OSError(
            "mock exception behavior")
        self.mockOs.path.exists.return_value = True
        self.mockOs.listdir.return_value = [
            u'history.js', u'reactComponents.js']

        javascript_bundler.bundle()
        self.mockSubprocessCall.assert_called_once_with(
            ['yarn', 'run', 'bundle:dev'])

        self.__assertState(javascript_bundler, JsState.OLD)

    def __assertState(self, javascript_bundler, expected_state):
        javascript_bundler.report() | should.equal(expected_state)
