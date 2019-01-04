from designate.objects import base
from designate.objects import fields

@base.DesignateRegistry.register
class RBACBaseObject(base.DictObjectMixin, base.PersistentObjectMixin,
                     base.DesignateObject):

    # not to confuse action field as all other Designate Objects
    # rbac_action is intended for allowed/denied actions
    # such as access_as_shared
    fields = {
        'id': common_types.UUIDField(),
        'project_id': obj_fields.StringField(),
        'object_id': common_types.UUIDField(),
        'target_tenant': obj_fields.StringField(),
        'rbac_action': obj_fields.StringField(),
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
