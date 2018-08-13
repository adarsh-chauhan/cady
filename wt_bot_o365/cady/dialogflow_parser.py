import json
from .ms_office import msoffice
from .conf import conf
from .users import onboarded_users


class apiai():

	def parser(self, json_data):
		ou = onboarded_users()
		ms=msoffice()
		user = json_data['originalDetectIntentRequest']['payload']['data']['data']['personEmail']

		if json_data['queryResult']['intent']['displayName'] == 'ms_calendar':
			if user in str(ou.users):
				return ms.readcalendar(user, json_data['queryResult']['parameters']['date'])
			else:
				return ms.onboarduser(user)
		return True 
