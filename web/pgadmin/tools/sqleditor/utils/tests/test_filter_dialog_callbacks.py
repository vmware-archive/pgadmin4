#######################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should

from pgadmin.tools.sqleditor.utils.filter_dialog import FilterDialog

TX_ID_ERROR_MSG = 'Transaction ID not found in the session.'
FAILED_TX_MSG = 'Failed to update the data on server.'


class MockRequest(object):
    "To mock request object"
    def __init__(self):
        self.data = None
        self.args = "Test data",


class TestStartRunningDataSorting:
    def test_filter_dialog_get_no_id(self):
        """
        When the FilterDialog.get method is called
        And there is no Transaction ID found in session
        It retuns a 404
        """
        result = FilterDialog.get(None, TX_ID_ERROR_MSG, None, None, None)
        result.status_code | \
            should.equal(404)

    def test_filter_dialog_get_no_values(self):
        """
        When the FilterDialog.get method is called
        And all the values are passed as None
        It retuns a 404
        """
        result = FilterDialog.get(None, None, None, None, None)
        result.status_code | \
            should.equal(200)

    def test_filter_dialog_save_no_id(self):
        """
        When the FilterDialog.save method is called
        And there is no Transaction ID found in session
        It retuns a 404
        """
        input_arg_parameters = (None, TX_ID_ERROR_MSG, None, None, None)
        input_kwarg_parameters = {
            'trans_id': None,
            'request': MockRequest()
        }

        result = FilterDialog.save(
            *input_arg_parameters, **input_kwarg_parameters)

        result.status_code | \
            should.equal(404)

    def test_filter_dialog_save_no_values(self):
        """
        When the FilterDialog.save method is called
        And all the values are passed as None
        It retuns a 500
        """
        input_arg_parameters = (None, None, None, None, None)
        input_kwarg_parameters = {
            'trans_id': None,
            'request': MockRequest()
        }

        result = FilterDialog.save(
            *input_arg_parameters, **input_kwarg_parameters)

        result.status_code | \
            should.equal(500)
