from django.shortcuts import render, redirect
from .dialogflow_parser  import apiai
from .ms_office import msoffice
from .conf import conf
import json,requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.


config = conf()

@csrf_exempt
def dialogflow(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		df = apiai()
		payload = df.parser(json_data)
		return JsonResponse(payload)

def authorize(request):
	if request.method == 'GET':
		user = request.GET.get('user',None)
		return redirect('https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&response_type=code&redirect_uri={1}&scope=offline_access%20user.read%20Calendars.Read&state={2}'.format(config.app_id, config.ngrok_url+'/cady/token',user))


def token(request):
	if request.method == 'GET':
		if request.GET.get('code',None):
			user = request.GET.get('state',None)
			ms = msoffice()
			if ms.get_accesstoken(user, request.GET.get('code',None)):
				return render(request,'onboarding.html')
			else:
				return render(request,'error.html')
