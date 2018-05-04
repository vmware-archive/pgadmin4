/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////
import {TreeFake} from '../tree/tree_fake';
import {menuEnabled} from '../../../pgadmin/static/js/menu/menu_enabled';

const context = describe;
describe('#menuEnabled', () => {
  let ourBrowser;
  beforeEach(() => {
    const tree = new TreeFake();
    ourBrowser = {
      treeMenu: tree,
    };
    tree.addNewNode('level1', {}, undefined, []);
    tree.addNewNode('level1.1', {_type: 'catalog'}, undefined, ['level1']);
    tree.addNewNode('level1.1.1', {_type: 'database'}, undefined, ['level1', 'level1.1']);
    tree.addNewNode('level1.2', {_type: 'bamm'}, undefined, ['level1']);
    tree.addNewNode('level1.2.1', {
      _type: 'database',
      allowConn: true,
    }, undefined, ['level1', 'level1.2']);
    tree.addNewNode('level1.2.2', {
      _type: 'database',
      allowConn: false,
    }, undefined, ['level1', 'level1.2']);
    tree.addNewNode('level1.2.3', {
      _type: 'table',
    }, undefined, ['level1', 'level1.2']);

    tree.addNewNode('level2', {}, undefined, []);
    tree.addNewNode('level2.1', null, undefined, ['level2']);
    tree.addNewNode('level2.1.1', {}, undefined, ['level2', 'level2.1']);
  });

  context('When the current node is a root node', () => {
    it('return false', () => {
      expect(menuEnabled(ourBrowser.treeMenu, [], {}, [{id: 'level1'}])).toBe(false);
    });
  });

  context('when current node does not exist', () => {
    it('return false', () => {
      expect(menuEnabled(ourBrowser.treeMenu, [], {}, [{id: 'bamm'}])).toBe(false);
    });
  });

  context('provided node data is undefined', () => {
    it('returns false', () => {
      expect(menuEnabled(ourBrowser.treeMenu, [], undefined, [{id: 'level1'}])).toBe(false);
    });
  });

  context('provided node data is null', () => {
    it('returns false', () => {
      expect(menuEnabled(ourBrowser.treeMenu, [], null, [{id: 'level1'}])).toBe(false);
    });
  });

  context('When the current node is not a root node', () => {
    context('parent data does not exist', () => {
      it('returns false', () => {
        expect(menuEnabled(ourBrowser.treeMenu, [], {}, [{id: 'level2.1.1'}])).toBe(false);
      });
    });

    context('parent as data', () => {
      context('the current node type is in the supported node types', () => {
        context('the parent is of the type catalog', () => {
          it('returns false', () => {
            expect(menuEnabled(ourBrowser.treeMenu,
              ['schema'],
              {_type: 'schema'},
              [{id: 'level1.1.1'}]
            )).toBe(false);
          });
        });
        context('an ancestor with type catalog exists', () => {
          it('returns false', () => {
            expect(menuEnabled(ourBrowser.treeMenu,
              ['table'],
              {_type: 'table'},
              [{id: 'level1.1.1.1'}]
            )).toBe(false);
          });
        });
        context('the parent is not of the type catalog', () => {
          context('current node is of the type database', () => {
            context('current node allows connection', () => {
              it('returns true', () => {
                expect(menuEnabled(ourBrowser.treeMenu,
                    ['database'],
                  {
                    _type: 'database',
                    allowConn: true,
                  }, [{id: 'level1.2.1'}])).toBe(true);
              });
            });
            context('current node do not allow connection', () => {
              it('returns false', () => {
                expect(menuEnabled(ourBrowser.treeMenu,
                    ['database'], {
                      _type: 'database',
                      allowConn: false,
                    }, [{id: 'level1.2.2'}])).toBe(false);
              });
            });
          });
          context('current node is not of the type database', () => {
            it('returns true', () => {
              expect(menuEnabled(ourBrowser.treeMenu,
                  ['schema'], {
                    _type: 'schema',
                  }, [{id: 'level1.2.3'}])).toBe(true);
            });
          });
        });
      });
      context('the current node type is not in the supported node types', () => {
        it('returns false', () => {
          expect(menuEnabled(ourBrowser.treeMenu, [], {_type: 'catalog'}, [{id: 'level1.1'}])).toBe(false);
        });
      });
    });
  });
});
