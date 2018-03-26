/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

export const backupSupportedNodes = [
  'database', 'schema', 'table', 'partition',
];

function isNodeTypeSupported(nodeDataType, parentNodeType) {
  return _.indexOf(backupSupportedNodes, nodeDataType) !== -1
    && parentNodeType !== 'catalog';
}

function isProvidedDataValid(treeNodeData) {
  return !_.isUndefined(treeNodeData) && !_.isNull(treeNodeData);
}

function doesNodeHaveMenu(treeNodeData) {
  return (treeNodeData._type === 'database' && treeNodeData.allowConn)
    || treeNodeData._type !== 'database';
}

function retrieveParentNodeType(treeNode) {
  if (!treeNode.hasParent()) {
    return null;
  }
  return treeNode.parent().getData()._type;
}

export function menuEnabled(treeNodeData, domTreeNode) {
  let treeNode = this.treeMenu.findNodeByDomElement(domTreeNode);
  let parentNodeType = retrieveParentNodeType(treeNode);

  if (isProvidedDataValid(treeNodeData) && !_.isNull(parentNodeType)) {
    return isNodeTypeSupported(treeNodeData._type, parentNodeType)
      && doesNodeHaveMenu(treeNodeData);
  } else {
    return false;
  }
}

function isNodeAServerAndConnected(treeNodeData) {
  return (('server' === treeNodeData._type) && treeNodeData.connected);
}

export function menuEnabledServer(treeNodeData) {
  return isProvidedDataValid(treeNodeData)
    && isNodeAServerAndConnected(treeNodeData);
}
