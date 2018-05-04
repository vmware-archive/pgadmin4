/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

function isNodeTypeSupported(backupSupportedNodes, nodeDataType, treeNode) {
  return _.indexOf(backupSupportedNodes, nodeDataType) !== -1
    && ancestorWithTypeCatalogDoesNotExists(treeNode);
}

export function isProvidedDataValid(treeNodeData) {
  return !_.isUndefined(treeNodeData) && !_.isNull(treeNodeData);
}

function doesNodeHaveMenu(treeNodeData) {
  return (treeNodeData._type === 'database' && treeNodeData.allowConn)
    || treeNodeData._type !== 'database';
}

function ancestorWithTypeCatalogDoesNotExists(treeNode) {
  let currentNode = treeNode;

  while(currentNode.hasParent() && treeNode.parent().getData() !== null) {
    if(currentNode.parent().getData()._type === 'catalog') {
      return false;
    }

    currentNode = currentNode.parent();
  }

  return true;
}

export function menuEnabled(tree, backupSupportedNodes, treeNodeData, domTreeNode) {
  let treeNode = tree.findNodeByDomElement(domTreeNode);
  if (!treeNode) {
    return false;
  }

  if (isProvidedDataValid(treeNodeData)) {
    return isNodeTypeSupported(backupSupportedNodes, treeNodeData._type, treeNode)
      && doesNodeHaveMenu(treeNodeData);
  } else {
    return false;
  }
}


