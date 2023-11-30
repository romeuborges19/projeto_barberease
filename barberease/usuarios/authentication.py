from datetime import datetime, timedelta
import jwt

def create_acess_token(id_usuario):
    return jwt.encode({
        'id_usuario': id_usuario,
        'exp': datetime.utcnow() + timedelta(seconds=12000),
        'iat': datetime.now()
    }, 'refresh_secret', algorithm='HS256')

def get_acess_token(token):
    return jwt.decode(token, 'refresh_secret', algorithms=['HS256'])

def get_token_user_id(request):
    jwt_token = request.COOKIES.get('jwt_token')

    if jwt_token:
        payload = get_acess_token(jwt_token)
        id_usuario = payload.get('id_usuario')
    else:
        id_usuario = 0

    return id_usuario
