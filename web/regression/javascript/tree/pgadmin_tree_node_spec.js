//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

import {getTreeNodeHierarchy} from "../../../pgadmin/static/js/tree/pgadmin_tree_node";
import {Tree} from "../../../pgadmin/static/js/tree/tree";

const context = describe;

describe('tree#node#getTreeNodeHierarchy', () => {
  let browser;
  let newTree;
  let translateTreeNodeIdFromACITreeSpy;
  beforeEach(() => {
    newTree = new Tree();
    browser = {
      Nodes: {
        'special one': {hasId: true},
        'child special': {hasId: true},
        'other type': {hasId: true},
        'table': {hasId: true},
        'partition': {hasId: true},
        'no id': {hasId: false},
      }
    };
    browser.treeMenu = newTree;
    translateTreeNodeIdFromACITreeSpy = spyOn(newTree, 'translateTreeNodeIdFromACITree');
  });

  describe('When the current node is root element', () => {
    beforeEach(() => {
      newTree.addNewNode('root', {
        'some key': 'some value',
        '_type': 'special one'
      }, []);
      translateTreeNodeIdFromACITreeSpy.and.returnValue(['root']);
    });

    it('returns a object with the element type passed data and priority == 0', () => {
      const result = getTreeNodeHierarchy.bind(browser)('root');
      expect(result).toEqual({
        'special one': {
          'some key': 'some value',
          '_type': 'special one',
          'priority': 0,
        }
      });
    });
  });

  describe('When the current node is not of a known type', () => {
    beforeEach(() => {
      newTree.addNewNode('root', {
        'some key': 'some value',
        '_type': 'do not exist'
      }, []);
      translateTreeNodeIdFromACITreeSpy.and.returnValue(['root']);
    });

    it('returns a empty object', () => {
      const result = getTreeNodeHierarchy.bind(browser)('root');
      expect(result).toEqual({});
    });
  });

  describe('When the current node type has no id', () => {
    beforeEach(() => {
      newTree.addNewNode('root', {
        'some key': 'some value',
        '_type': 'no id'
      }, []);
      translateTreeNodeIdFromACITreeSpy.and.returnValue(['root']);
    });

    it('returns a empty object', () => {
      const result = getTreeNodeHierarchy.bind(browser)('root');
      expect(result).toEqual({});
    });
  });

  describe('When the current node is at the second level', () => {
    beforeEach(() => {
      newTree.addNewNode('root', {
        'some key': 'some value',
        '_type': 'special one'
      }, []);
      newTree.addNewNode('first child', {
        'some key': 'some other value',
        '_type': 'child special'
      }, ['root']);
      translateTreeNodeIdFromACITreeSpy.and.returnValue(['root', 'first' +
      ' child']);
    });

    it('returns a empty object', () => {
      const result = getTreeNodeHierarchy.bind(browser)('first child');
      expect(result).toEqual({
        'child special': {
          'some key': 'some other value',
          '_type': 'child special',
          'priority': 0,
        },
        'special one': {
          'some key': 'some value',
          '_type': 'special one',
          'priority': -1,
        },
      });
    });
  });

  context('When tree as "special type"', () => {
    context('When "special type" have "other type"', () => {
      context('When "other type" have "special type"', () => {
        describe('When retrieving lead node', () => {
          it('does not override previous node type data', () => {
            newTree.addNewNode('root', {
              'some key': 'some value',
              '_type': 'special one'
            }, []);
            newTree.addNewNode('level 1', {
              'some key': 'some value',
              '_type': 'other type'
            }, ['root']);
            newTree.addNewNode('level 2', {
              'some key': 'expected value',
              '_type': 'special one',
              'some other key': 'some other value',
            }, ['root', 'level 1']);

            translateTreeNodeIdFromACITreeSpy.and.returnValue(['root', 'level 1', 'level 2']);

            const result = getTreeNodeHierarchy.bind(browser)('level 2');
            expect(result).toEqual({
              'special one': {
                'some key': 'expected value',
                '_type': 'special one',
                'some other key': 'some other value',
                'priority': 0,
              },
              'other type': {
                'some key': 'some value',
                '_type': 'other type',
                'priority': -1,
              },
            });
          });
        });
      });
    });
  });

  context('When tree has table', () => {
    context('when table has partition', () => {
      it('returns table with partition parameters', () => {
        newTree.addNewNode('root', {
          'some key': 'some value',
          '_type': 'special one'
        }, []);
        newTree.addNewNode('level 1', {
          'some key': 'some value',
          '_type': 'table'
        }, ['root']);
        newTree.addNewNode('level 2', {
          'some key': 'expected value',
          '_type': 'partition',
          'some other key': 'some other value',
        }, ['root', 'level 1']);

        translateTreeNodeIdFromACITreeSpy.and.returnValue(['root', 'level 1', 'level 2']);

        const result = getTreeNodeHierarchy.bind(browser)('level 2');
        expect(result).toEqual({
          'special one': {
            'some key': 'some value',
            '_type': 'special one',
            'priority': -1,
          },
          'table': {
            'some key': 'expected value',
            'some other key': 'some other value',
            '_type': 'partition',
            'priority': 0,
          },
        });
      });

    });

  });
});
