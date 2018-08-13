
class onboarded_users():
	users = []

	def __init__(self):
		self.email = ''
		self.name = ''
		self.access_token = ''
		self.refresh_token = ''
		self.scope = ''
		self.token_type = ''
		self.expires_in = ''
		self.ext_expires_in = ''
		self.onboarding_completed = False

	def __repr__(self):
		return str(self.email)

	def load_user(self, obj, email, data):	
		self.email = email
		self.access_token = data['access_token']
		self.refresh_token = data['refresh_token']
		#for k in data.keys():
		#	self.k = data[k]
		#	print(self.k)
		self.users.append(self)
		self.onboarding_completed = True
		print("users: onboarduser : Onboarded Users List : " + str(self.users))
		return True
