from django.shortcuts import render
import json

def index(request):
    user = request.user
    if user.is_authenticated():
        bootstrap_json = dict()
        bootstrap_json['username'] = user.username

        if bool(user.photo) is False:
            bootstrap_json['avatar'] = ""
        else:
            bootstrap_json['avatar'] = user.photo.url
        bootstrap_json['points'] = user.points


        context = {
            'bootstrap_json': json.dumps(bootstrap_json),
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'auth.html', dict())

def make_error_handler(code, status):
    def error_handler(request):
        return render(request, 'error.html', dict(
            code=code,
            status=status
        ))
    return error_handler
