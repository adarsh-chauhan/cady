import requests, datetime
from .conf import conf
from .users import onboarded_users

config = conf()

class msoffice():
	def __init__(self):
		#config.bot_accesstoken = self.get_bot_accesstoken()
		pass	

	def readcalendar(self,user, querytime):
                
		#url='https://graph.microsoft.com/beta/me/calendar/events?$select=subject,organizer,start,end,location'
		ou = onboarded_users()
		
		for i in ou.users:
			if i.email == user:
				access_token = i.access_token
		
		querytime = datetime.datetime.strptime(querytime.split('+')[0],'%Y-%m-%dT%H:%M:%S').isoformat()
		queryendtime = datetime.datetime.strptime(querytime.split('+')[0],'%Y-%m-%dT%H:%M:%S').date().isoformat() + 'T23:59:59'
		
		url = 'https://graph.microsoft.com/beta/me/calendar/calendarView?startDateTime={0}&endDateTime={1}'.format(querytime,queryendtime)
		
		headers = {'Prefer': 'outlook.timezone="Asia/Kolkata"','Authorization': 'Bearer ' + access_token}
		
		reply = requests.get(url, headers=headers)
		
		events=reply.json()['value']
		meetings = ['0',]
		for i in events:
			temp = {}
			temp['organizer'] = i['organizer']['emailAddress']['name']
			temp['subject'] = i['subject']
			temp['start'] = i['start']
			temp['end'] = i['end']
			temp['location'] = i['location']['displayName']
			temp['weblink'] = i['webLink']
			meetings.append(temp)
		meetings.reverse()
		final_text = ''
		if len(meetings) > 1:
			for n,i in enumerate(meetings):
				if i != '0':
					text = '({num}): **Organiser**: {org}, Subject: {sub}, Starts at: {start}, Location: {loc}\n For more info: {web}\n\n'.format(num=n, org=i['organizer'], sub=i['subject'], start=i['start'], loc=i['location'], web=i['weblink'])
					final_text = text + final_text	
		else:
			final_text = 'You know whats the best thing about today, No Meetings!'
		return {"fulfillmentMessages":[{"text":{"text":[final_text]}}]}


	def get_accesstoken (self, email, code):
		url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
		payload = {
			'client_id': config.app_id,
			'scope' : 'calendars.read',
			'code': code,
			'redirect_uri': config.ngrok_url + '/cady/token',
			'grant_type' : 'authorization_code',
			'client_secret': config.app_pass
			}
		reply = requests.post(url,data=payload)
		data = reply.json()
		print(data)
		ou = onboarded_users()
		if str(reply.status_code) == '200' and ou.load_user(ou ,email, data):
			return True
		else:
			return False
    	
	def get_bot_accesstoken(self):
		url = 'https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token'
		payload = {
			'grant_type': 'client_credentials', 
			'client_id': config.app_id, 
			'client_secret' : config.app_pass, 
			'scope' : 'https://api.botframework.com/.default'
			}

		reply = requests.post(url,data=payload)

		if str(reply.status_code) == '200':
			config.bot_accesstoken = reply.json()['access_token']
			print('msoffice: Bot Access Token Fetched!')
			return config.bot_accesstoken
		else:
			print('msoffice: Error retrieving Bot Accesstoken! : {0}'.format(reply.text))
			return False


	def onboarduser(self,email):
		return {"fulfillmentMessages":[{"text":{"text":["Let's onboard you first so that I have permissions to access your data:\n {0}/cady/authorize?user={1}".format(config.ngrok_url,email)]}}]}

