//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

export function getTreeNodeHierarchyFromElement(pgBrowser, treeNode) {
  return getTreeNodeHierarchy.call(pgBrowser, treeNode);
}

export function getTreeNodeHierarchyFromIdentifier(aciTreeNodeIdentifier) {
  let identifier = this.treeMenu.translateTreeNodeIdFromACITree(aciTreeNodeIdentifier);
  let currentNode = this.treeMenu.findNode(identifier);
  return getTreeNodeHierarchy.call(this, currentNode);
}

export function getTreeNodeHierarchy(currentNode) {
  let idx = 0;
  let result = {};

  do {
    const currentNodeData = currentNode.getData();
    if (currentNodeData._type in this.Nodes && this.Nodes[currentNodeData._type].hasId) {
      const nodeType = mapType(currentNodeData._type);
      if (result[nodeType] === undefined) {
        result[nodeType] = _.extend({}, currentNodeData, {
          'priority': idx,
        });
        idx -= 1;
      }
    }
    currentNode = currentNode.hasParent() ? currentNode.parent() : null;
  } while (currentNode);

  return result;
}

function mapType(type) {
  return type === 'partition' ? 'table' : type;
}
