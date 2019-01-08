import re

import pecan
from oslo_log import log as logging

from designate import utils
from designate import exceptions
from designate import objects
from designate.objects.adapters import DesignateAdapter
from designate.objects import RBACBaseObject
from designate.api.v2.controllers import rest

LOG = logging.getLogger(__name__)

class RbacController(rest.RestController):

    @pecan.expose(template='json:', content_type='application/json')
    @utils.validate_uuid('rbac_id')
    def get_one(self, rbac_id):
        """Get RBAC parameter"""

        request = pecan.request
        context = request.environ['context']

        rbacrule = self.central_api.get_rbacrule(context, rbac_id)

        LOG.info("Retrieved %(rbacrule)s", {'rbacrule': rbacrule})

        return DesignateAdapter.render('API_v2', rbacrule, request=request)

    
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

        rules = self.central_api.list_rbac_rules(object_id=object_id,
                                                 project_id=project_id)

        LOG.info("Retrieved %(rbacrules)s", {'rbacrules': rules})

        return DesignateAdapter.render('API_v2', rules, request=request)

    @pecan.expose(template='json:', content_type='application/json')
    def post_all(self):
        request = pecan.request
        response = pecan.response
        context = request.environ['context']

        body = request.body_dict
        rbac_obj = DesignateAdapter.parse('API_v2', body, RBACBaseObject())
        
        rbac_obj.validate()

        # Create the blacklist
        rbac_obj = self.central_api.create_rbacrule(
            context, rbac_obj)

        LOG.info("Created %(rbac)s", {'rbac': rbac_obj})

        response.status_int = 201

        rbac_obj = DesignateAdapter.render(
            'API_v2', rbac_obj, request=request)

        #response.headers['Location'] = rbac_obj['links']['self']

        # Prepare and return the response body
        return rbac


    @pecan.expose(template='json:', content_type='application/json')
    @pecan.expose(template='json:', content_type='application/json-patch+json')
    @utils.validate_uuid('rbac_id')
    def patch_one(self, rbac_id):
        """Update RBAC rule"""
        request = pecan.request
        context = request.environ['context']
        body = request.body_dict
        response = pecan.response

        if request.content_type == 'application/json-patch+json':
            raise NotImplemented('json-patch not implemented')

        # Fetch the existing rbac entry
        rbac = self.central_api.get_rbacrule(context, rbac_id)

        rbac = DesignateAdapter.parse('API_v2', body, rbac)

        rbac.validate()

        rbac = self.central_api.update_rbacrule(context, rbac)

        LOG.info("Updated %(rbac)s", {'rbac': rbac})

        response.status_int = 200

        return DesignateAdapter.render('API_v2', rbac, request=request)

    
    @pecan.expose(template=None, content_type='application/json')
    @utils.validate_uuid('rbac_id')
    def delete_one(self, rbac_id):
        """Delete Rbac Zone"""
        request = pecan.request
        response = pecan.response
        context = request.environ['context']

        rbac = self.central_api.delete_rbacrule(context, rbac_id)

        LOG.info("Deleted %(rbac)s", {'rbac': rbac})

        response.status_int = 204

        # NOTE: This is a hack and a half.. But Pecan needs it.
        return ''

        
