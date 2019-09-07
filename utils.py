def generate_html_people(items, result_file_name):
    template_text = open('template.html', 'r').read()
    output_file = open(result_file_name, 'w')

    tag_start = '$item_start$'
    tag_end = '$item_end$'

    container_start = template_text.find(tag_start)
    container_end = template_text.find(tag_end) + len(tag_end)


    output_file.write(template_text[:container_start])

    person_template = template_text[container_start + len(tag_start):container_end - len(tag_end)]
    for item in items:
        tmp = person_template.replace('$link$', item.get('person_link'))
        tmp = tmp.replace('$image$', item.get('image_link'))
        output_file.write(tmp)

    output_file.write(template_text[container_end:])

    output_file.close()

def check_proxies(proxy_file_name):
    import requests
    proxies = []
    with open(proxy_file_name, 'r') as file:
        for line in file:
            bits = line.strip().split('\t')[:2]
            proxies.append('http://' + ':'.join(bits))

    def test_proxy(proxy):
        p = {
          'http': proxy,
          'https': proxy,
        }

        try:
            r = requests.get('https://vk.com', proxies=p, timeout=2)
            print('good ' + str(p))
            return proxy
        except:
            return None


    # return test_proxy(proxies[0])

    from pathos.multiprocessing import ProcessingPool as Pool
    with Pool(processes=20) as pool:
        ar = [x for x in pool.map(test_proxy, proxies) if x is not None]
        ar = [x for x in pool.map(test_proxy, ar) if x is not None]
        ar = [x for x in pool.map(test_proxy, ar) if x is not None]

        return ar


if __name__ == '__main__':
    # print(check_proxies('proxy_list.txt'))

    good = ['http://144.217.204.254:3128', 'http://181.215.238.184:8080', 'http://195.4.154\
    .160:3128', 'http://206.189.192.206:3128', 'http://89.236.17.106:3128', 'http://\
    217.61.104.140:3128', 'http://165.227.5.215:8080', 'http://173.212.240.181:3128'\
    , 'http://195.49.200.154:8080', 'http://206.189.33.170:8080', 'http://80.211.189\
    .165:3128', 'http://35.161.133.86:8080', 'http://192.116.142.153:8080', 'http://\
    78.25.68.13:8080', 'http://13.114.76.47:3128', 'http://66.70.206.225:3128', 'htt\
    p://51.15.227.220:3128', 'http://110.136.49.154:8080', 'http://36.77.250.148:808\
    0', 'http://66.82.123.234:8080', 'http://81.200.22.135:8080']





