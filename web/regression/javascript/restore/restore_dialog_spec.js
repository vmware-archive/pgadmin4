/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////
import {TreeFake} from '../tree/tree_fake';
import {
  RestoreDialog,
} from '../../../pgadmin/static/js/restore/restore_dialog';
import {TreeNode} from '../../../pgadmin/static/js/tree/tree';

const context = describe;

describe('RestoreDialog', () => {
  let restoreDialog;
  let pgBrowser;
  let jquerySpy;
  let alertifySpy;
  let restoreModelSpy;


  let rootNode;
  let serverTreeNode;
  let databaseTreeNode;
  let ppasServerTreeNode;
  let noDataNode;

  beforeEach(() => {
    pgBrowser = {
      treeMenu: new TreeFake(),
      Nodes: {
        server: jasmine.createSpyObj('Node[server]', ['getTreeNodeHierarchy']),
        database: jasmine.createSpyObj('Node[database]', ['getTreeNodeHierarchy']),
      },
    };
    pgBrowser.Nodes.server.hasId = true;
    pgBrowser.Nodes.database.hasId = true;
    jquerySpy = jasmine.createSpy('jquerySpy');
    restoreModelSpy = jasmine.createSpy('restoreModelSpy');

    rootNode = pgBrowser.treeMenu.addNewNode('level1', {}, [{id: 'level1'}], []);
    serverTreeNode = new TreeNode('level1.1', {
      _type: 'server',
      _id: 10,
      label: 'some-tree-label',
    }, [{id: 'level1.1'}]);
    pgBrowser.treeMenu.addChild(rootNode, serverTreeNode);

    databaseTreeNode = new TreeNode('level1.1.1', {
      _type: 'database',
      _id: 10,
      _label: 'some-database-label',
    }, [{id: 'level1.1.1'}], ['level1', 'level1.1']);
    pgBrowser.treeMenu.addChild(serverTreeNode, databaseTreeNode);

    ppasServerTreeNode = new TreeNode('level1.2', {
      _type: 'server',
      server_type: 'ppas',
    }, [{id: 'level1.2'}], ['level1']);
    pgBrowser.treeMenu.addChild(rootNode, ppasServerTreeNode);

    const level3 = new TreeNode('level3', {}, [{id: 'level3'}]);
    pgBrowser.treeMenu.addChild(ppasServerTreeNode, level3);

    noDataNode = pgBrowser.treeMenu.addNewNode('level3.1', undefined, [{id: 'level1'}]);
    pgBrowser.treeMenu.addChild(level3, noDataNode);

  });

  describe('#draw', () => {
    beforeEach(() => {
      alertifySpy = jasmine.createSpyObj('alertify', ['alert', 'dialog']);
      alertifySpy['pg_restore'] = jasmine.createSpy('pg_restore');
      restoreDialog = new RestoreDialog(
        pgBrowser,
        jquerySpy,
        alertifySpy,
        restoreModelSpy
      );

      pgBrowser.get_preference = jasmine.createSpy('get_preferences');
    });

    context('there are no ancestors of the type server', () => {
      it('does not create a dialog', () => {
        pgBrowser.treeMenu.selectNode([{id: 'level1'}]);
        restoreDialog.draw(null, null, null);
        expect(alertifySpy['pg_restore']).not.toHaveBeenCalled();
      });

      it('display an alert with a Restore Error', () => {
        restoreDialog.draw(null, [{id: 'level1'}], null);
        expect(alertifySpy.alert).toHaveBeenCalledWith(
          'Restore Error',
          'Please select server or child node from the browser tree.'
        );
      });
    });

    context('there is an ancestor of the type server', () => {
      context('no preference can be found', () => {
        beforeEach(() => {
          pgBrowser.get_preference.and.returnValue(undefined);
        });

        context('server is a ppas server', () => {
          it('display an alert with "Restore Error"', () => {
            restoreDialog.draw(null, [serverTreeNode], null);
            expect(alertifySpy.alert).toHaveBeenCalledWith(
              'Restore Error',
              'Failed to load preference pg_bin_dir of module paths'
            );
          });
        });

        context('server is not a ppas server', () => {
          it('display an alert with "Restore Error"', () => {
            restoreDialog.draw(null, [ppasServerTreeNode], null);
            expect(alertifySpy.alert).toHaveBeenCalledWith(
              'Restore Error',
              'Failed to load preference ppas_bin_dir of module paths'
            );
          });
        });
      });

      context('preference can be found', () => {
        context('binary folder is not configured', () => {
          beforeEach(() => {
            pgBrowser.get_preference.and.returnValue({});
          });

          context('server is a ppas server', () => {
            it('display an alert with "Configuration required"', () => {
              restoreDialog.draw(null, [serverTreeNode], null);
              expect(alertifySpy.alert).toHaveBeenCalledWith(
                'Configuration required',
                'Please configure the PostgreSQL Binary Path in the Preferences dialog.'
              );
            });
          });

          context('server is not a ppas server', () => {
            it('display an alert with "Configuration required"', () => {
              restoreDialog.draw(null, [ppasServerTreeNode], null);
              expect(alertifySpy.alert).toHaveBeenCalledWith(
                'Configuration required',
                'Please configure the EDB Advanced Server Binary Path in the Preferences dialog.'
              );
            });
          });
        });

        context('binary folder is configured', () => {
          let spy;
          beforeEach(() => {
            spy = jasmine.createSpyObj('globals', ['resizeTo']);
            alertifySpy['pg_restore'].and
              .returnValue(spy);
            pgBrowser.get_preference.and.returnValue({value: '/some/path'});
            pgBrowser.Nodes.server.label = 'some-server-label';
          });

          it('displays the dialog', () => {
            restoreDialog.draw(null, [{id: 'level1.1'}], {server: true});
            expect(alertifySpy['pg_restore']).toHaveBeenCalledWith(
              'Restore (some-server-label: some-tree-label)',
              [{id: 'level1.1'}],
              serverTreeNode.getData(),
              pgBrowser.Nodes.server
            );
            expect(spy.resizeTo).toHaveBeenCalledWith('65%', '60%');
          });
        });
      });
    });
  });
});
