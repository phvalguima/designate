import re

import pecan
from oslo_log import log as logging

from designate import exceptions
from designate import objects
from designate.objects.adapters import DesignateAdapter
from designate.objects import RBACBaseObject
from designate.api.v2.controllers import rest

LOG = logging.getLogger(__name__)

class RbacController(rest.RestController):

    @pecan.expose(template='json:', content_type='application/json')
    def get_all(self, **params):
        """List RBAC rules that comply with either object or project ids for a Tenant"""
        request = pecan.request
        context = request.environ['context']

        object_id = None
        project_id = None

        try:
            body = request.body_dict
            rbac_obj = DesignateAdapter.parse('API_v2', body, RBACBaseObject())
            object_id = rbac_obj.object_id
            project_id = rbac_obj.project_id
        except Exception as e:
            if str(e) != 'TODO: Unsupported Content Type':
                raise
            else:
                # Got a blank body
                body = dict() 

        #rules = self.central_api.list_rbac_rules(object_id=object_id,
        #                                         project_id=project_id)

        LOG.info("Retrieved %(rbacrules)s", {'rbacrules': rules})

        return DesignateAdapter.render('API_v2', rules, request=request)
