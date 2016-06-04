from django.shortcuts import render
from django.http import HttpResponse
from flashcrowd.users.models import CustomUser
import json

# Create your views here.
def index(request):
    user = request.user
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

def make_error_handler(code, status):
    def error_handler(request):
        return render(request, 'error.html', dict(
            code=code,
            status=status
        ))
    return error_handler
