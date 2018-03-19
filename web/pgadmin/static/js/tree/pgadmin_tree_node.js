//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

export function getTreeNodeHierarchy(aciTreeIdentifier) {
  let idx = 0;
  let result = {};
  let identifier = this.treeMenu.translateTreeNodeIdFromACITree(aciTreeIdentifier);
  let currentNode = this.treeMenu.findNode(identifier);
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
