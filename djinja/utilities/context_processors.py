def request_path(request):
    # los devolvemos en la variable de contexto "settings"
    return {'request_path': request.path}