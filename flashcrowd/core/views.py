from django.shortcuts import render
from django.http import HttpResponse
from django.render import loader
from users.models import CustomUser
import json

# Create your views here.
def index(request):
    user = request.user
    bootstrap_json = dict()
    bootstrap_json['username'] = user.username
    bootstrap_json['avatar'] = user.photo.url
    bootstrap_json['points'] = user.points

    template = loader.get_template('index.html')
    context = {
        'bootstrap_json': json.dumps(bootstrap_json),
    }
    return HttpResponse(template.render(context, request))