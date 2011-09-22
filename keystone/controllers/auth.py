from keystone import utils
from keystone.common import wsgi
from keystone.logic.types import auth
import keystone.config as config


class AuthController(wsgi.Controller):
    """Controller for token related operations"""

    def __init__(self, options):
        self.options = options

    @utils.wrap_error
    def authenticate(self, req):
        auth_with_credentials = utils.get_normalized_request_content(
            auth.AuthWithPasswordCredentials, req)

        return utils.send_result(200, req,
            config.SERVICE.authenticate(auth_with_credentials))

    @utils.wrap_error
    def authenticate_ec2(self, req):
        creds = utils.get_normalized_request_content(auth.Ec2Credentials, req)
        return utils.send_result(200, req,
            config.SERVICE.authenticate_ec2(creds))

    def _validate_token(self, req, token_id):
        """Validates the token, and that it belongs to the specified tenant"""
        belongs_to = req.GET.get('belongsTo')
        return config.SERVICE.validate_token(
            utils.get_auth_token(req), token_id, belongs_to)

    @utils.wrap_error
    def validate_token(self, req, token_id):
        result = self._validate_token(req, token_id)
        return utils.send_result(200, req, result)

    @utils.wrap_error
    def check_token(self, req, token_id):
        """Validates the token, but only returns a status code (HEAD)"""
        self._validate_token(req, token_id)
        return utils.send_result(200, req)

    @utils.wrap_error
    def delete_token(self, req, token_id):
        return utils.send_result(204, req,
            config.SERVICE.revoke_token(utils.get_auth_token(req), token_id))

    @utils.wrap_error
    def endpoints(self, req, token_id):
        x = utils.send_result(200, req,
            config.SERVICE.get_endpoints_for_token(utils.get_auth_token(req),
                                                   token_id))
        return x
