from django.utils.deprecation import GetResponseCallable, MiddlewareMixin
from authentication import verify_token

class TokenCheckMiddleware(MiddlewareMixin):
    # Verifica se o token do usuário é válido e existir
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()
        
    
    def __call__(self, request):
        response = self.get_response(request)
        return response 