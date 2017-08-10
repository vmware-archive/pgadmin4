//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2017, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////
import queryToolActions from 'sources/sqleditor/query_tool_actions';

describe('queryToolActions', () => {
  let sqlEditorControllerSpy,
    getSelectionSpy, getValueSpy,
    selectedQueryString, entireQueryString;

  describe('executeQuery', () => {
    describe('when the command is being run from the query tool', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_clearMessageTab');
      });

      it('clears the html in the message tab', () => {
        queryToolActions.executeQuery(sqlEditorControllerSpy);

        expect(queryToolActions._clearMessageTab).toHaveBeenCalled();
      });

      it('calls the execute function on the sqlEditorControllerSpy', () => {
        queryToolActions.executeQuery(sqlEditorControllerSpy);

        expect(sqlEditorControllerSpy.execute).toHaveBeenCalled();
      });
    });
    describe('when the command is being run from the view data view', () => {
      beforeEach(() => {
        setUpSpies('', '');
        sqlEditorControllerSpy.is_query_tool = false;
      });

      it('it calls the execute_data_query function on the sqlEditorControllerSpy', () => {
        queryToolActions.executeQuery(sqlEditorControllerSpy);

        expect(sqlEditorControllerSpy.execute_data_query).toHaveBeenCalled();
      });

    });
  });

  describe('explainAnalyze', () => {
    describe('when verbose and costs are not selected and buffers and timing are not selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('OFF');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('OFF');
        spyOn(queryToolActions, '_buffers').and.returnValue('OFF');
        spyOn(queryToolActions, '_timing').and.returnValue('OFF');
      });
      it('calls the execute function', () => {
        queryToolActions.explainAnalyze(sqlEditorControllerSpy);
        let explainAnalyzeQuery = 'EXPLAIN (FORMAT JSON, ANALYZE ON, VERBOSE OFF, COSTS OFF, BUFFERS OFF, TIMING OFF) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainAnalyzeQuery);
      });
    });

    describe('when verbose and costs and buffers and timing are all selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('ON');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('ON');
        spyOn(queryToolActions, '_buffers').and.returnValue('ON');
        spyOn(queryToolActions, '_timing').and.returnValue('ON');
      });
      it('calls the execute function', () => {
        queryToolActions.explainAnalyze(sqlEditorControllerSpy);
        let explainAnalyzeQuery = 'EXPLAIN (FORMAT JSON, ANALYZE ON, VERBOSE ON, COSTS ON, BUFFERS ON, TIMING ON) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainAnalyzeQuery);
      });
    });

    describe('when verbose is selected and costs is not selected and buffer is selected and timing is not selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('ON');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('OFF');
        spyOn(queryToolActions, '_buffers').and.returnValue('ON');
        spyOn(queryToolActions, '_timing').and.returnValue('OFF');
      });
      it('calls the execute function', () => {
        queryToolActions.explainAnalyze(sqlEditorControllerSpy);
        let explainAnalyzeQuery = 'EXPLAIN (FORMAT JSON, ANALYZE ON, VERBOSE ON, COSTS OFF, BUFFERS ON, TIMING OFF) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainAnalyzeQuery);
      });
    });

    describe('when verbose is  not selected and costs is selected and buffer is not selected and timing is  selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('OFF');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('ON');
        spyOn(queryToolActions, '_buffers').and.returnValue('OFF');
        spyOn(queryToolActions, '_timing').and.returnValue('ON');
      });
      it('calls the execute function', () => {
        queryToolActions.explainAnalyze(sqlEditorControllerSpy);
        let explainAnalyzeQuery = 'EXPLAIN (FORMAT JSON, ANALYZE ON, VERBOSE OFF, COSTS ON, BUFFERS OFF, TIMING ON) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainAnalyzeQuery);
      });
    });
  });

  describe('explain', () => {
    describe('when verbose and costs are selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('ON');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('ON');
      });
      it('calls the execute function', () => {
        queryToolActions.explain(sqlEditorControllerSpy);
        let explainQuery = 'EXPLAIN (FORMAT JSON, ANALYZE OFF, VERBOSE ON, COSTS ON, BUFFERS OFF, TIMING OFF) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainQuery);
      });
    });

    describe('when verbose and costs are not selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('OFF');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('OFF');
      });
      it('calls the execute function', () => {
        queryToolActions.explain(sqlEditorControllerSpy);
        let explainQuery = 'EXPLAIN (FORMAT JSON, ANALYZE OFF, VERBOSE OFF, COSTS OFF, BUFFERS OFF, TIMING OFF) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainQuery);
      });
    });

    describe('when verbose is selected and costs is not selected', () => {
      beforeEach(() => {
        setUpSpies('', '');
        spyOn(queryToolActions, '_verbose').and.returnValue('ON');
        spyOn(queryToolActions, '_costsEnabled').and.returnValue('OFF');
      });
      it('calls the execute function', () => {
        queryToolActions.explain(sqlEditorControllerSpy);
        let explainQuery = 'EXPLAIN (FORMAT JSON, ANALYZE OFF, VERBOSE ON, COSTS OFF, BUFFERS OFF, TIMING OFF) ';
        expect(sqlEditorControllerSpy.execute).toHaveBeenCalledWith(explainQuery);
      });
    });
  });

  describe('download', () => {
    describe('when the query is empty', () => {
      beforeEach(() => {
        setUpSpies('', '');
      });
      it('does nothing', () => {
        queryToolActions.download(sqlEditorControllerSpy);

        expect(sqlEditorControllerSpy.trigger_csv_download).not.toHaveBeenCalled();
      });
    });

    describe('when the table was opened through the queryTool', () => {
      describe('when the query tool object has a selection', () => {
        let time;

        beforeEach(() => {
          entireQueryString = 'include some more of that yummy string cheese;';
          selectedQueryString = 'some silly string cheese';
          setUpSpies(selectedQueryString, entireQueryString);

          time = 'rightNow';
          spyOn(window, 'Date').and.callFake(() => ({
            getTime: () => {
              return time;
            },
          }));
        });

        it('calls trigger_csv_download with the query and the filename', () => {
          let filename = 'data-' + time + '.csv';

          queryToolActions.download(sqlEditorControllerSpy);

          expect(sqlEditorControllerSpy.trigger_csv_download).toHaveBeenCalledWith(selectedQueryString, filename);
        });
      });

      describe('when there is no selection', () => {
        let time;

        beforeEach(() => {
          selectedQueryString = '';
          entireQueryString = 'include some more of that yummy string cheese;';

          setUpSpies(selectedQueryString, entireQueryString);

          time = 'rightNow';
          spyOn(window, 'Date').and.callFake(() => ({
            getTime: () => {
              return time;
            },
          }));
        });

        it('calls trigger_csv_download with the query and the filename', () => {
          let filename = 'data-' + time + '.csv';

          queryToolActions.download(sqlEditorControllerSpy);

          expect(sqlEditorControllerSpy.trigger_csv_download).toHaveBeenCalledWith(entireQueryString, filename);
        });
      });
    });

    describe('when the table was opened through tables, view all data', () => {
      it('calls trigger_csv_download with the sqlQuery and the table name', () => {
        let query = 'a very long query';
        setUpSpies('', query);
        sqlEditorControllerSpy.is_query_tool = false;

        queryToolActions.download(sqlEditorControllerSpy);

        expect(sqlEditorControllerSpy.trigger_csv_download).toHaveBeenCalledWith(query, 'iAmATable' + '.csv');
      });
    });

  });

  describe('commentBlockCode', () => {
    describe('when there is no query text', () => {
      beforeEach(() => {
        setUpSpies('', '');
      });
      it('does nothing', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.commentBlockCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.toggleComment).not.toHaveBeenCalled();
      });
    });

    describe('when there is empty selection', () => {
      beforeEach(() => {
        setUpSpies('', 'a string\nddd\nsss');

        sqlEditorControllerSpy.gridView.query_tool_obj.getCursor = (isFrom) => {
          return isFrom ? 3 : 3;
        };
      });

      it('comments the current line', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.commentBlockCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.toggleComment).toHaveBeenCalledWith(3, 3);
      });
    });

    describe('when some part of the query is selected', () => {
      beforeEach(() => {
        setUpSpies('a string\nddd', 'a string\nddd\nsss');
      });

      it('comments the selection', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.commentBlockCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.toggleComment).toHaveBeenCalledWith(0, 12);
      });
    });
  });

  describe('commentLineCode', () => {
    describe('when there is no query text', () => {
      beforeEach(() => {
        setUpSpies('', '');
      });
      it('does nothing', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.commentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.lineComment).not.toHaveBeenCalled();
      });
    });

    describe('when there is empty selection', () => {
      beforeEach(() => {
        setUpSpies('', 'a string\nddd\nsss');

        sqlEditorControllerSpy.gridView.query_tool_obj.getCursor = (isFrom) => {
          return isFrom ? 3 : 3;
        };
      });

      it('comments the current line', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;
        queryToolActions.commentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.lineComment).toHaveBeenCalledWith(3, 3, {lineComment: '--'});
      });
    });

    describe('when some part of the query is selected', () => {
      beforeEach(() => {
        setUpSpies('tring\nddd', 'a string\nddd\nsss');
      });

      it('comments the selection', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.commentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.lineComment).toHaveBeenCalledWith(3, 12, {lineComment: '--'});
      });
    });
  });

  describe('uncommentLineCode', () => {
    describe('when there is no query text', () => {
      beforeEach(() => {
        setUpSpies('', '');
      });
      it('does nothing', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.uncommentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.uncomment).not.toHaveBeenCalled();
      });
    });

    describe('when there is empty selection', () => {
      beforeEach(() => {
        setUpSpies('', 'a string\nddd\nsss');

        sqlEditorControllerSpy.gridView.query_tool_obj.getCursor = (isFrom) => {
          return isFrom ? 3 : 3;
        };
      });

      it('uncomments the current line', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.uncommentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.uncomment).toHaveBeenCalledWith(3, 3, {lineComment: '--'});
      });
    });

    describe('when some part of the query is selected', () => {
      beforeEach(() => {
        setUpSpies('tring\nddd', 'a string\nddd\nsss');
      });

      it('uncomments the selection', () => {
        let codeMirrorObj = sqlEditorControllerSpy.gridView.query_tool_obj;

        queryToolActions.uncommentLineCode(sqlEditorControllerSpy);

        expect(codeMirrorObj.uncomment).toHaveBeenCalledWith(3, 12, {lineComment: '--'});
      });
    });
  });

  describe('formatSql', () => {
    describe('when there is empty selection', () => {
      beforeEach(() => {
        setUpSpies('', 'a string\nddd\nsss');

        sqlEditorControllerSpy.gridView.query_tool_obj.getCursor = (isFrom) => {
          return isFrom ? 3 : 3;
        };
      });

      it('formats the entire sql editor text', () => {
        const sqlFormatterSpy = jasmine.createSpyObj('sqlFormatter', ['parse']);
        sqlFormatterSpy.parse.and.returnValue('correctly FORMATTED SQL string');

        queryToolActions.formatSql(sqlEditorControllerSpy, sqlFormatterSpy);

        expect(sqlFormatterSpy.parse).toHaveBeenCalledWith('a string\nddd\nsss');
        expect(sqlEditorControllerSpy.gridView.query_tool_obj.setValue)
          .toHaveBeenCalledWith('correctly FORMATTED SQL string');
      });
    });

    describe('when some part of the query is selected', () => {
      beforeEach(() => {
        setUpSpies('tring\nddd', 'a string\nddd\nsss');
      });

      it('formats the entire sql editor text', () => {
        const sqlFormatterSpy = jasmine.createSpyObj('sqlFormatter', ['parse']);
        sqlFormatterSpy.parse.and.returnValue('correctly FORMATTED SQL string');

        queryToolActions.formatSql(sqlEditorControllerSpy, sqlFormatterSpy);

        expect(sqlFormatterSpy.parse).toHaveBeenCalledWith('a string\nddd\nsss');
        expect(sqlEditorControllerSpy.gridView.query_tool_obj.setValue)
          .toHaveBeenCalledWith('correctly FORMATTED SQL string');
      });
    });
  });


  function setUpSpies(selectedQueryString, entireQueryString) {
    getValueSpy = jasmine.createSpy('getValue').and.returnValue(entireQueryString);
    getSelectionSpy = jasmine.createSpy('getSelection').and.returnValue(selectedQueryString);

    sqlEditorControllerSpy = {
      gridView: {
        query_tool_obj: {
          getSelection: getSelectionSpy,
          getValue: getValueSpy,
          setValue: jasmine.createSpy('setValue'),
          toggleComment: jasmine.createSpy('toggleComment'),
          lineComment: jasmine.createSpy('lineComment'),
          uncomment: jasmine.createSpy('uncomment'),
          getCursor: (isFrom) => {
            return entireQueryString.indexOf(selectedQueryString) + (isFrom ? 0 : selectedQueryString.length);
          },
        },
      },
      trigger_csv_download: jasmine.createSpy('trigger_csv_download'),
      trigger: jasmine.createSpy('trigger'),
      table_name: 'iAmATable',
      is_query_tool: true,
      execute: jasmine.createSpy('execute'),
      execute_data_query: jasmine.createSpy('execute_data_query'),
      formatSql: jasmine.createSpy('formatSql'),
    };
  }
});
