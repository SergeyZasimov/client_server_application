from datetime import datetime

def validate_request(request):
    return 'action' in request  and 'time' in request and request.get('action') and request.get('time')

def make_response(request, code, data=None, date=datetime.now()):
    return{
        'action':request.get('action'),
        'time': date.timestamp(),
        'code': code,
        'data': data
    }

def make_400(request, data=None, date=datetime.now()):
    return make_response(request, 400, data, date)

def make_500(request, date=datetime.now()):
    return make_response(request, 500, 'Internal server error', date)

def make_404(request, data, date=datetime.now()):
    return make_response(request, 400, data, date)