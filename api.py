from mongo import (
        db,
        get_db_data,
        load_db_data,
        update_db_data,
        )

from mail import (
        send_confirmation_email,
        send_reset_key_email,
        )

from key_gen import generate_api_key
import json
from responder import API
from apispec import APISpec, yaml_utils
from apispec.ext.marshmallow import MarshmallowPlugin
import maya

contact = {
        'name': 'Productivity in Tech',
        'url': 'https://productivityintech.com',
        'email': 'info@productivityintech.com',
        }

api_description = '''This is the Conftalks.dev Public API. It is used to manage
your alerts!
'''

api_key_scheme = {'type': 'apiKey', 
                'in': 'header',
                'name': 'api_key',
                }

class API(API):
    @property
    def _apispec(self):

        info = {}
        if self.description is not None:
            info["description"] = self.description
        if self.terms_of_service is not None:
            info["termsOfService"] = self.terms_of_service
        if self.contact is not None:
            info["contact"] = self.contact
        if self.license is not None:
            info["license"] = self.license

        spec = APISpec(
            title=self.title,
            version=self.version,
            openapi_version=self.openapi_version,
            plugins=[MarshmallowPlugin()],
            info=info,
            )
        spec.components.security_scheme("api_key", api_key_scheme)

        for route in self.routes:
            if self.routes[route].description:
                operations = yaml_utils.load_operations_from_docstring(
                    self.routes[route].description
                )
                spec.path(path=route, operations=operations)

        for name, schema in self.schemas.items():
            spec.components.schema(name, schema=schema)


        return spec
    
api = API(
        title='Conftalks API',
        version='0.1',
        openapi='3.0.2',
        docs_route='/',
        contact=contact,
        description=api_description,
        )

@api.route(before_request=True)
def auth_required(req, resp, user_data={}):
    api_key = {'api_key': req.headers.get('authorization')}
    if api_key:
        user_data = get_db_data('users', filter_by=api_key, return_one=True)
        req.headers.update({'user_data': user_data})


if __name__ == '__main__': 
    from events import *
    from users import *
    from conferences import *
    api.run(debug=True)
