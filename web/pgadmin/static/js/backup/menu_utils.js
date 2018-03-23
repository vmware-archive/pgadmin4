/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

var backup_supported_nodes = [
  'database', 'schema', 'table', 'partition',
];

export function menu_enabled(itemData, item) {
  let t = this.tree,
    i = item,
    d = itemData,
    parent_item = t.hasParent(i) ? t.parent(i) : null,
    parent_data = parent_item ? t.itemData(parent_item) : null;

  if (!_.isUndefined(d) && !_.isNull(d) && !_.isNull(parent_data)) {
    if (_.indexOf(backup_supported_nodes, d._type) !== -1 &&
      parent_data._type != 'catalog') {
      if (d._type == 'database' && d.allowConn)
        return true;
      else if (d._type != 'database')
        return true;
      else
        return false;
    } else
      return false;
  } else
    return false;
}
