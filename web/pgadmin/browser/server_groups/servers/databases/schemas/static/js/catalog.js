define('pgadmin.node.catalog', [
  'sources/gettext', 'jquery', 'underscore', 'underscore.string', 'pgadmin',
  'pgadmin.browser', 'backform', 'alertify', 'pgadmin.browser.collection'
], function(gettext, $, _, S, pgAdmin, pgBrowser, Backform, alertify) {

  // Extend the browser's collection class for catalog collection
  if (!pgBrowser.Nodes['coll-catalog']) {
    var databases = pgBrowser.Nodes['coll-catalog'] =
      pgBrowser.Collection.extend({
        node: 'catalog',
        label: gettext('Catalogs'),
        type: 'coll-catalog',
        columns: ['name', 'namespaceowner', 'description']
      });
  };
  // Extend the browser's node class for catalog node
  if (!pgBrowser.Nodes['catalog']) {
    pgBrowser.Nodes['catalog'] = pgBrowser.Node.extend({
      parent_type: 'database',
      type: 'catalog',
      label: gettext('Catalog'),
      hasSQL:  true,
      hasDepends: true,
      Init: function() {
        /* Avoid mulitple registration of menus */
        if (this.initialized)
            return;

        this.initialized = true;

      },
      model: pgBrowser.Node.Model.extend({
        defaults: {
          name: undefined,
          namespaceowner: undefined,
          nspacl: undefined,
          description: undefined,
          securitylabel: []
        },
        initialize: function(attrs, args) {
          var isNew = (_.size(attrs) === 0);

          if (isNew) {
            var userInfo = pgBrowser.serverInfo[args.node_info.server._id].user;

            this.set({'namespaceowner': userInfo.name}, {silent: true});
          }
          pgBrowser.Node.Model.prototype.initialize.apply(this, arguments);
        },
        schema: [{
          id: 'name', label: gettext('Name'), cell: 'string',
          type: 'text', disabled: true
        },{
          id: 'oid', label: gettext('OID'), cell: 'string', mode: ['properties'],
          type: 'text', disabled: true
        },{
          id: 'namespaceowner', label: gettext('Owner'), cell: 'string',
          type: 'text', disabled: true
        },{
          id: 'acl', label: gettext('Privileges'), type: 'text',
          group: gettext('Security'), mode: ['properties'], disabled: true
        },{
          id: 'description', label: gettext('Comment'), cell: 'string',
          type: 'multiline'
       },{
          id: 'seclabels', label: gettext('Security Labels'),
          model: pgBrowser.SecLabelModel, editable: false, type: 'collection',
          group: gettext('Security'), mode: ['edit', 'create'],
          min_version: 90200, canAdd: true,
          canEdit: false, canDelete: true, control: 'unique-col-collection'
         }
        ],
        validate: function() {
          return null;
        }
      })
  });

  }

  return pgBrowser.Nodes['catalog'];
});
