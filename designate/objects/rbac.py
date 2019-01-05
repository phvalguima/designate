from designate.objects import base
from designate.objects import fields

@base.DesignateRegistry.register
class RBACBaseObject(base.DictObjectMixin, base.PersistentObjectMixin,
                     base.DesignateObject):

    # not to confuse action field as all other Designate Objects
    # rbac_action is intended for allowed/denied actions
    # such as access_as_shared
    fields = {
        'id': fields.UUIDFields(nullable=False),
        'project_id': fields.UUIDFields(nullable=False),
        'object_id': fields.UUIDFields(nullable=True),
        'target_tenant': fields.UUIDFields(nullable=True),
        'rbac_action': fields.StringFields(maxLength=255), 
    }

    fields_no_update = ['id', 'project_id', 'object_id']

    STRING_KEYS = [
        'id', 'project_id', 'object_id', 'target_tenant', 'rbac_action'
    ]

    @classmethod
    def get_projects(cls, context, object_id=None, action=None,
                     target_tenant=None):
        ## TODO: update this method as it was done with:
        ## https://github.com/openstack/neutron/blob/master/neutron/objects/rbac.py#L44
        return None


@base.DesignateRegistry.register
class RBACBaseObjectList(base.ListObjectMixin, base.DesignateObject):
    LIST_ITEM_TYPE = RBACBaseObject

    fields = {
	'objects': fields.ListOfObjectsField('RBACBaseObject'),
    }
