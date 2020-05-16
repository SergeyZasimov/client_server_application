from protocol import make_200

def echo_controller(request):
    return make_200(request, request.get('data'))