import json
import requests
from people import *

def get_friends(id, count = 1000):
    from requests import get

    url = 'https://api.vk.com/method/friends.get'
    par = {
    'user_id' : str(id),
    'count' : count,
    'offset' : 0,
    'fields' : 'bdate,city,relation,can_write_private_message,sex,can_send_friend_request,followers_count,photo_max',
    'v' : '5.60'
    }

    return extract_people(get(url, params = par).json())

def get_people_from_group_id(group_id, count, offset):
	from stalker import make_request

	url = 'https://api.vk.com/method/groups.getMembers'
	payload = {
		'group_id' : str(group_id),
		'count' : str(count),
		'offset' : str(offset),
		'v' : '5.60'
	}

	response = make_request(url, payload)

	ids = response.get('response', {}).get('items', [])
	return get_people_for_ids(ids)

	
def get_people_for_ids(ids):
	from stalker import make_request

	url ='https://api.vk.com/method/users.get'
	payload = {
		'user_ids' : ','.join([str(id) for id in ids]),
		'fields' : 'bdate,city,relation,can_write_private_message,sex,can_send_friend_request,followers_count,photo_max',
		'name_case' : 'Nom',
		'v' : '5.60'
	}

	response = make_request(url, payload)
	return exctract_people_from_json(response)

def compute_stats_for_person(person):
	friends = get_friends(person['id'], count = 1000)

	cities = {}
	years = {}

	for friend in friends:
		if 'bdate' in friend:
			bdate = friend['bdate']
		else:
			bdate = ''

		if 'city_id' in friend:
			city = friend['city_id']
		else:
			city = -1

		if bdate != '':
			ar = bdate.strip().split('.')
			if len(ar) == 3:
				if ar[2] in years:
					years[ar[2]] = years[ar[2]] + 1
				else:
					years[ar[2]] = 1

		if city != -1:
			if city in cities:
				cities[city] = cities[city] + 1
			else:
				cities[city] = 1

	max = 0
	max_id = 0
	for id, c in cities.items():
		if c > max:
			max = c
			max_id = id

	print('max city: ' + str(max_id) + ' with count: ' + str(max))
	person['computed_city_id'] = max_id
	person['computed_city_count'] = max 

	max_c = 0
	max_year = ''
	for year, count in years.items():
		if count > max_c:
			max_c = count
			max_year = year

	person['computed_year'] = max_year
	person['computed_year_count'] = max_c		
	print('max year: ' + str(max_year) + ' with count: ' + str(max_c))
	print(years)

def get_people_for_count_and_offset(inp):
	group_id, count, offset = inp
	if count == 0:
		return []
		
	response = get_people_from_group_id(group_id, count, offset)

	if len(response) == 0:
		return []


	target_city_id = 1
	target_years = {'2000', '1998', '1999'}
	followers_min_count = 50
	followers_max_count = 300
	sex = 1



	res = []
	for person in response:
		if person.sex != sex: continue
		if person.city_id != target_city_id : continue
		if person.year != 0:
			if person.year not in target_years: continue
		if person.followers_count != 0:
			if person.followers_count < followers_min_count or person.followers_count > followers_max_count:
				continue
		if person.can_write_private_message == 0: continue

		res.append(person)
	return res

def get_subscribers_from_group_id_with_filter(group_id, count, offsett):
	people = []
	offset = offsett

	response_count = 250
	def get_counts_and_offsets(count, offset):
		res = []
		current_offset = offset
		border = offset + count
		while True:
			if current_offset + response_count <= border:
				res.append((response_count, current_offset))
				current_offset += response_count
			elif current_offset < border:
				res.append((border - current_offset, current_offset))
				return res
			else:
				return res

	from multiprocessing import Pool
	with Pool(processes = 9) as pool:
		counts_and_offsets = get_counts_and_offsets(count, offset)
		people = pool.map(get_people_for_count_and_offset, [(group_id, count, offset) for count, offset in counts_and_offsets])




	res = []
	for arr in people:
		res.extend(arr)
	print("total people: {}".format(len(res)))
	return res



if __name__ == "__main__":
	import utils

	people = []
	count = 5000
	offset = 10000
	group_id = 139111933

	items = []

	while True:

		people = get_subscribers_from_group_id_with_filter(group_id, count, offset)
		offset += count

		for person in people:
			items.append({
				'image_link' : person.photo,
				'person_link' : 'https://vk.com/id' + str(person.id)
				})

		utils.generate_html_people(items, 'output.html')
		print('html generated')







	