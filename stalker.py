access_token = '38fc65ccc365e0712b219a8ed8afd0d8b2553d250c02c39d22c33bf04db6bf8bd6e1ab4e926228109c5a7'
my_id = 
add_ids = []

def make_request(url, payload, timeout=2, proxy=None):
	from requests import get
	from time import sleep

	if proxy is not None:
		p = {
		  'http': proxy,
		  'https': proxy,
		}
	else:
		p = None

	while True:
		try:
			r = get(url, params=payload, timeout=timeout, proxies=p)
			try:
				resp = r.json()
			except Exception as e:
				print('could not parse json')
				print(url, payload, len(payload.get('user_ids').split(',')))
				print(r.text)
				print(e)
				continue
			if r.status_code == 200:
				if 'error' in resp:
					if resp.get('error').get('error_code') == 6:
						sleep(1)
						continue
					print('error ' + str(resp.get('error')))
					sleep(1)
					continue
				break
		except Exception as e:
			print(e)
	return resp

def get_friends(user_id):
	payload = {
		'user_id' : str(user_id),
		'v' : '5.74',
		'access_token' : access_token
	}
	resp = make_request('https://api.vk.com/method/friends.get', payload)
	return resp.get('response').get('items')

def get_online_friends(user_id, proxy=None):
	payload = {
		'user_id' : str(user_id),
		'online_mobile' : '1',
		'v' : '5.74',
		'access_token' : access_token
	} 
	response = make_request('https://api.vk.com/method/friends.getOnline', payload, timeout=2).get('response')
	return response.get('online'), response.get('online_mobile', None)

def permanent_online():
	from time import sleep, ctime
	payload = {
		'voip' : '0',
		'access_token' : access_token,
		'v' : '5.74',
	}
	while True:
		r = make_request('https://api.vk.com/method/account.setOnline', payload)
		print('[{}] online set'.format(ctime()))
		sleep(30)		


if __name__ == '__main__':

	# print(permanent_online())
	# quit()

	sleep_time = 60*4


	import time

	all_ids_to_check = get_friends(my_id)
	all_ids_to_check.append(my_id)
	all_ids_to_check.extend(add_ids)

	while True:
		start = time.time()
		from multiprocessing import Pool
		with Pool(processes=6) as pool:
		    ars = pool.map(get_online_friends, [id for id in all_ids_to_check])
		ar = []
		ar_mob = []
		for arr in ars:
			ar.extend([x for x in arr[0] if x not in ar])
			ar_mob.extend([x for x in arr[1] if x is not None and x not in ar_mob])

		with open('online_log.txt', 'a') as file:
			file.write(str(time.time()) + ';')
			file.write(','.join([str(id) for id in ar]) + ';')
			file.write(','.join([str(id) for id in ar_mob]) + '\n')
		end = time.time()

		time_to_process = end - start
		print('time took:', time_to_process)
		print('sleeping now for', str(sleep_time - time_to_process))

		time.sleep(sleep_time - time_to_process)



	# print(ar)
	# print(len(ar))
	# print(time_to_process)
