##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import sys

import simplejson as json
from flask import Response
from grappa import should

from pgadmin.tools.sqleditor.utils.start_running_query import StartRunningQuery
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.exception import ConnectionLost, SSHTunnelConnectionLost

if sys.version_info < (3, 3):
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock

get_driver_exception = Exception('get_driver exception')
get_connection_lost_exception = Exception('Unable to connect to server')


class TestStartRunningQuery:

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_no_griddata(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And gridData is not present in session
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'

        manager = self.__create_manager(
            False,
            None,
            None,
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict()
        )

        result | should.equal(expected_response)
        make_json_response_mock.assert_called_with(
            success=0,
            errormsg='Transaction ID not found in the session.',
            info='DATAGRID_TRANSACTION_REQUIRED',
            status=404
        )
        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_no_transaction_id(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the transactionID is not present in the gridData
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'

        manager = self.__create_manager(
            False,
            None,
            None,
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData=dict())
        )

        result | should.equal(expected_response)
        make_json_response_mock.assert_called_with(
            success=0,
            errormsg='Transaction ID not found in the session.',
            info='DATAGRID_TRANSACTION_REQUIRED',
            status=404
        )
        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_no_command_info(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the command information cannot be retrieved
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = None

        manager = self.__create_manager(
            False,
            None,
            None,
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)
        make_json_response_mock.assert_called_with(
            data=dict(
                status=False,
                result='Either transaction object or session object '
                       'not found.',
                can_edit=False,
                can_filter=False,
                info_notifier_timeout=5,
                notifies=None
            )
        )
        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_db_exception(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And exception happens while retrieving the database driver
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock()
        )

        self.__create_manager(
            False,
            None,
            None,
            None
        )
        get_driver_mock.side_effect = get_driver_exception

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)
        make_json_response_mock.assert_not_called()
        internal_server_error_mock.assert_called_with(
            errormsg='get_driver exception'
        )
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_called_with(
            get_driver_exception
        )
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_conn_lost(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And Connection is lost when retrieving the db connection
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock()
        )

        manager = self.__create_manager(
            False,
            None,
            None,
            ConnectionLost('1', '2', '3')
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        (lambda: StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )) | should.raises(ConnectionLost)

        make_json_response_mock.assert_not_called()
        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_sshconn_lost(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And SSHTunnelConnectionLost is lost when retrieving the db connection
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock()
        )

        manager = self.__create_manager(
            False,
            None,
            None,
            SSHTunnelConnectionLost('1.1.1.1')
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        (lambda: StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )) | should.raises(SSHTunnelConnectionLost)

        make_json_response_mock.assert_not_called()
        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_fail_to_connect(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And failure to connect to the server occurs
        it returns an error
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response
        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock()
        )

        self.__create_manager(
            False,
            [False, 'Unable to connect to server'],
            None,
            None
        )
        get_driver_mock.side_effect = get_connection_lost_exception

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)

        make_json_response_mock.assert_not_called()
        internal_server_error_mock.assert_called_with(
            errormsg='Unable to connect to server'
        )
        self.connection.execute_async.assert_not_called()
        loggerMock.error.assert_called_with(
            get_connection_lost_exception
        )
        self.connection.execute_void.assert_not_called()

    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.update_session_grid_transaction')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_fail_to_connect(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        update_session_grid_transaction_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the server is connected and start query async
        it returns a success message
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response

        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock(),
            set_connection_id=MagicMock(),
            auto_commit=True,
            auto_rollback=False,
            can_edit=lambda: True,
            can_filter=lambda: True
        )

        manager = self.__create_manager(
            False,
            None,
            [True, 'async function result output'],
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)

        make_json_response_mock.assert_called_with(
            data=dict(
                status=True,
                result='async function result output',
                can_edit=True,
                can_filter=True,
                info_notifier_timeout=5,
                notifies=None
            )
        )

        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_called_with(
            'some sql'
        )
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_not_called()

        apply_explain_plan_wrapper_if_needed_mock.assert_called_with(
            manager,
            dict(sql='some sql', explain_plan=None)
        )

    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.update_session_grid_transaction')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_begin_required(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        update_session_grid_transaction_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the server is connected and start query async
        And begin is required
        it returns a success message
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response

        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=True)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=False)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock(),
            set_connection_id=MagicMock(),
            auto_commit=True,
            auto_rollback=False,
            can_edit=lambda: True,
            can_filter=lambda: True
        )

        manager = self.__create_manager(
            False,
            None,
            [True, 'async function result output'],
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)

        make_json_response_mock.assert_called_with(
            data=dict(
                status=True,
                result='async function result output',
                can_edit=True,
                can_filter=True,
                info_notifier_timeout=5,
                notifies=None
            )
        )

        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_called_with(
            'some sql'
        )
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_called_with(
            'BEGIN;'
        )

        apply_explain_plan_wrapper_if_needed_mock.assert_called_with(
            manager,
            dict(sql='some sql', explain_plan=None)
        )

    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.update_session_grid_transaction')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_rollback_required(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        update_session_grid_transaction_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the server is connected and start query async
        And rollback is required
        it returns a success message
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response

        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=True)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'some sql'
        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock(),
            set_connection_id=MagicMock(),
            auto_commit=True,
            auto_rollback=False,
            can_edit=lambda: True,
            can_filter=lambda: True
        )

        manager = self.__create_manager(
            False,
            None,
            [True, 'async function result output'],
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)

        make_json_response_mock.assert_called_with(
            data=dict(
                status=True,
                result='async function result output',
                can_edit=True,
                can_filter=True,
                info_notifier_timeout=5,
                notifies=None
            )
        )

        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_called_with(
            'some sql'
        )
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_called_with(
            'ROLLBACK;'
        )

        apply_explain_plan_wrapper_if_needed_mock.assert_called_with(
            manager,
            dict(sql='some sql', explain_plan=None)
        )

    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.update_session_grid_transaction')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.pickle')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query.get_driver')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.apply_explain_plan_wrapper_if_needed')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.internal_server_error')
    @patch('pgadmin.tools.sqleditor.utils.start_running_query'
           '.make_json_response')
    def test_start_query_with_plan_wrapper(
        self,
        make_json_response_mock,
        internal_server_error_mock,
        apply_explain_plan_wrapper_if_needed_mock,
        get_driver_mock,
        pickle_mock,
        update_session_grid_transaction_mock,
        request
    ):
        """
        When StartRunningQuery is executed
        And the server is connected and start query async
        And an explain plan wrapper
        it returns a success message
        """

        request.addfinalizer(self.tearDown)

        expected_response = \
            Response(response=json.dumps({'errormsg': 'some value'}))
        make_json_response_mock.return_value = expected_response

        StartRunningQuery.is_begin_required_for_sql_query = \
            MagicMock(return_value=False)
        StartRunningQuery.is_rollback_statement_required = \
            MagicMock(return_value=True)
        apply_explain_plan_wrapper_if_needed_mock.return_value = \
            'EXPLAIN PLAN some sql'

        pickle_mock.loads.return_value = MagicMock(
            conn_id=1,
            update_fetched_row_cnt=MagicMock(),
            set_connection_id=MagicMock(),
            auto_commit=True,
            auto_rollback=False,
            can_edit=lambda: True,
            can_filter=lambda: True
        )

        manager = self.__create_manager(
            False,
            None,
            [True, 'async function result output'],
            None
        )
        get_driver_mock.return_value = MagicMock(
            connection_manager=lambda session_id: manager)

        blueprint_mock = MagicMock(
            info_notifier_timeout=MagicMock(get=lambda: 5)
        )
        loggerMock = MagicMock(error=MagicMock())

        result = StartRunningQuery(
            blueprint_mock,
            loggerMock
        ).execute(
            sql=dict(sql='some sql', explain_plan=None),
            trans_id=123,
            http_session=dict(gridData={'123': dict(command_obj='')})
        )

        result | should.equal(expected_response)

        make_json_response_mock.assert_called_with(
            data=dict(
                status=True,
                result='async function result output',
                can_edit=True,
                can_filter=True,
                info_notifier_timeout=5,
                notifies=None
            )
        )

        internal_server_error_mock.assert_not_called()
        self.connection.execute_async.assert_called_with(
            'EXPLAIN PLAN some sql'
        )
        loggerMock.error.assert_not_called()
        self.connection.execute_void.assert_called_with(
            'ROLLBACK;'
        )

        apply_explain_plan_wrapper_if_needed_mock.assert_called_with(
            manager,
            dict(sql='some sql', explain_plan=None)
        )

    def __create_manager(
        self,
        is_connected_to_server,
        connection_connect_return,
        execute_async_return_value,
        manager_connection_exception
    ):
        self.connection = MagicMock(
            connected=lambda: is_connected_to_server,
            connect=MagicMock(),
            execute_async=MagicMock(),
            execute_void=MagicMock(),
            get_notifies=MagicMock(),
        )
        self.connection.connect.return_value = connection_connect_return
        self.connection.get_notifies.return_value = None
        self.connection.execute_async.return_value = \
            execute_async_return_value
        if manager_connection_exception is None:
            def connection_function(
                did,
                conn_id,
                use_binary_placeholder,
                array_to_string,
                auto_reconnect
            ):
                return self.connection

            manager = MagicMock(
                connection=connection_function
            )

        else:
            manager = MagicMock()
            manager.connection.side_effect = manager_connection_exception

        return manager

    def tearDown(self):
        StartRunningQuery.is_rollback_statement_required = False
