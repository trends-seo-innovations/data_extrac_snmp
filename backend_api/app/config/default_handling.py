from backend_api.app import app
from backend_api.app import jwt
from backend_api.app import blacklist

@app.errorhandler(404)
def page_not_found(e):
    return {'message': 'Not found', 'type': '404'}, 404

@app.errorhandler(500)
def page_not_found(e):
    return {'message': 'Internal Server Error', 'type': '500'}, 500

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


