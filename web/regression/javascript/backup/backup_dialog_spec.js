/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////
import {BackupDialog} from '../../../pgadmin/static/js/backup/backup_dialog';
import {TreeFake} from '../tree/tree_fake';
import {TreeNode} from '../../../pgadmin/static/js/tree/tree';

const context = describe;

describe('ObjectBackupDialog', () => {
  let backupDialog;
  let pgBrowser;
  let jquerySpy;
  let alertifySpy;
  let backupModelSpy;


  let rootNode;
  let serverTreeNode;
  let databaseTreeNode;
  let ppasServerTreeNode;
  let noDataNode;

  beforeEach(() => {
    pgBrowser = {
      treeMenu: new TreeFake(),
      Nodes: {
        server: {
          hasId: true,
          label: 'server',
          getTreeNodeHierarchy: jasmine.createSpy('server.getTreeNodeHierarchy'),
        },
        database: {
          hasId: true,
          label: 'database',
          getTreeNodeHierarchy: jasmine.createSpy('db.getTreeNodeHierarchy'),
        },
        schema: {
          hasId: true,
          label: 'schema',
          getTreeNodeHierarchy: jasmine.createSpy('db.getTreeNodeHierarchy'),
        },
      },
    };
    pgBrowser.Nodes.server.hasId = true;
    pgBrowser.Nodes.database.hasId = true;
    jquerySpy = jasmine.createSpy('jquerySpy');
    backupModelSpy = jasmine.createSpy('backupModelSpy');

    rootNode = pgBrowser.treeMenu.addNewNode('level1', {}, []);

    serverTreeNode = new TreeNode('level1.1', {
      _type: 'server',
      _id: 10,
    });
    pgBrowser.treeMenu.addChild(rootNode, serverTreeNode);

    databaseTreeNode = new TreeNode(
      'level1.1.1', {
        _type: 'database',
        _id: 11,
        label: 'some_database',
        _label: 'some_database_label',
      }, [{id: 'level1.1.1'}]);
    pgBrowser.treeMenu.addChild(serverTreeNode, databaseTreeNode);

    ppasServerTreeNode = new TreeNode('level1.2', {
      _type: 'server',
      server_type: 'ppas',
    });
    pgBrowser.treeMenu.addChild(rootNode, ppasServerTreeNode);

    const someNodeUnderneathPPASServer = new TreeNode('level3', {});
    pgBrowser.treeMenu.addChild(ppasServerTreeNode,
      someNodeUnderneathPPASServer);

    noDataNode = new TreeNode(
      'level3.1', undefined);
    pgBrowser.treeMenu.addChild(someNodeUnderneathPPASServer, noDataNode);
  });

  describe('#draw', () => {
    beforeEach(() => {
      alertifySpy = jasmine.createSpyObj('alertify', ['alert', 'dialog']);
      alertifySpy['backup_objects'] = jasmine.createSpy('backup_objects');
      backupDialog = new BackupDialog(
        pgBrowser,
        jquerySpy,
        alertifySpy,
        backupModelSpy
      );

      pgBrowser.get_preference = jasmine.createSpy('get_preferences');
    });

    context('there are no ancestors of the type server', () => {
      it('does not create a dialog', () => {
        pgBrowser.treeMenu.selectNode([rootNode]);
        backupDialog.draw(null, null, null);
        expect(alertifySpy['backup_objects']).not.toHaveBeenCalled();
      });

      it('display an alert with a Backup Error', () => {
        backupDialog.draw(null, [rootNode], null);
        expect(alertifySpy.alert).toHaveBeenCalledWith(
          'Backup Error',
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
          it('display an alert with "Backup Error"', () => {
            backupDialog.draw(null, [{id: 'level1.1.1'}], null);
            expect(alertifySpy.alert).toHaveBeenCalledWith(
              'Backup Error',
              'Failed to load preference pg_bin_dir of module paths'
            );
          });
        });

        context('server is not a ppas server', () => {
          it('display an alert with "Backup Error"', () => {
            backupDialog.draw(null, [ppasServerTreeNode], null);
            expect(alertifySpy.alert).toHaveBeenCalledWith(
              'Backup Error',
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
              backupDialog.draw(null, [serverTreeNode], null);
              expect(alertifySpy.alert).toHaveBeenCalledWith(
                'Configuration required',
                'Please configure the PostgreSQL Binary Path in the Preferences dialog.'
              );
            });
          });

          context('server is not a ppas server', () => {
            it('display an alert with "Configuration required"', () => {
              backupDialog.draw(null, [ppasServerTreeNode], null);
              expect(alertifySpy.alert).toHaveBeenCalledWith(
                'Configuration required',
                'Please configure the EDB Advanced Server Binary Path in the Preferences dialog.'
              );
            });
          });
        });

        context('binary folder is configured', () => {
          let backupDialogResizeToSpy;
          beforeEach(() => {
            backupDialogResizeToSpy = jasmine.createSpyObj('backupDialogResizeToSpy', ['resizeTo']);
            alertifySpy['backup_objects'].and
              .returnValue(backupDialogResizeToSpy);
            pgBrowser.get_preference.and.returnValue({value: '/some/path'});
          });

          it('displays the dialog', () => {
            backupDialog.draw(null, [serverTreeNode], null);
            expect(alertifySpy['backup_objects']).toHaveBeenCalledWith(true);
            expect(backupDialogResizeToSpy.resizeTo).toHaveBeenCalledWith('60%', '50%');
          });
        });
      });
    });
  });

});
