/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

import {isProvidedDataValid} from '../menu/menu_enabled';

export const backupSupportedNodes = [
  'database', 'schema', 'table', 'partition',
];

function isNodeAServerAndConnected(treeNodeData) {
  return (('server' === treeNodeData._type) && treeNodeData.connected);
}

export function menuEnabledServer(treeNodeData) {
  return isProvidedDataValid(treeNodeData)
    && isNodeAServerAndConnected(treeNodeData);
}
