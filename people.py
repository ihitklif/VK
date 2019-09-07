class Person:
	def __init__(self, id, first_name, last_name):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name

		self.photo = ''

		self.sex = 0

		self.can_write_private_message = 0
		self.can_send_friend_request = 0
		
		self.friends_count = 0
		self.followers_count = 0

		self.city_id = 0
		self.computed_city_id = 0

		self.year = 0
		self.computed_year = 0

	def print(self):
		print("Person: {} {}".format(self.first_name, self.last_name))
		print("  sex:  {}".format("male" if self.sex == 2 else "female" if self.sex == 1 else "??"))
		print('  city: {}'.format(get_city_title_for_id(self.city_id)))
		print("  year: {}".format(self.year if self.year != 0 else ''))
		print("  can_write: {}".format("yes" if self.can_write_private_message == 1 else 'no'))
		print('  followers: {}'.format(str(self.followers_count) if self.followers_count != 0 else ''))
		print('  comp_year: {}'.format(str(self.computed_year) if self.computed_year != 0 else ''))
		print('  comp_city: {}'.format(get_city_title_for_id(self.computed_city_id)))
		print('  photo: {}'.format(self.photo))
		print('  id:  {}'.format(str(self.id)))

		print('')

def exctract_people_from_json(json):
	if 'response' not in json:
		raise

	if 'items' not in json['response']:
		if len(json['response']) > 0:
			if 'id' in json['response'][0]:
				items = json['response']
			else:
				return []
		else:
			return []
	else:
		items = json['response']['items']


	people = [get_person_from_item(x) for x in items]

	return people

def get_person_from_item(item):
	first_name = item.get('first_name', 'first_name')
	last_name = item['last_name']
	id = item.get('id')

	person = Person(id, first_name, last_name)

	person.sex = 0 if 'sex' not in item else item['sex']
	person.year = '' if 'bdate' not in item else get_year_from_bdate(item['bdate'])
	person.photo = '' if 'photo_max' not in item else item['photo_max']

	if 'city' in item:
		person.city_id = item['city']['id']
		add_city_title_for_id(person.city_id, item['city']['title'])

	if 'can_write_private_message' in item:
		person.can_write_private_message = item['can_write_private_message']

	if 'can_send_friend_request' in item:
		person.can_send_friend_request = item['can_send_friend_request']

	if 'followers_count' in item:
		person.followers_count = item['followers_count']

	return person

def get_year_from_bdate(bdate):
	items = bdate.strip().split('.')
	if len(items[-1]) == 4:
		return items[-1]
	else:
		return ''

global city_titles
city_titles = {'' : ''}

def add_city_title_for_id(id, title):
	global city_titles
	if id not in city_titles:
		city_titles[id] = title

def get_city_title_for_id(id):
	global city_titles
	if id in city_titles:
		return city_titles[id]
	else: return ''