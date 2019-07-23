import requests
from urllib.parse import urlencode
import os
from hashlib import md5

headers = {
    'cookie': '__tasessionId=ampozol5g1563806844189; tt_webid=671649' +
    '9234256455175; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16c' +
    '1a26e5e12df-040ada0c1d8081-c343162-100200-16c1a26e5e428c; CNZZDAT' +
    'A1259612802=945869726-1563806204-https%253A%252F%252Fwww.google.c' +
    'om%252F%7C1563806204; tt_webid=6716499234256455175; csrftoken=46' +
    'a41d4141000920aea9354904736a2d; s_v_web_id=2b8f7242614ce9f3dd7cbf' +
    '26d932530d',
    'host': 'www.toutiao.com',
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit' +
    '/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


def get_page(offset):
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': '1563782026489'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('suc_1')
            # print(response.json())
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images:
                for image in images:
                    print('suc_2')
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }
    else:
        print('data is none')


def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        print('suc_3')
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(
                item.get('title'),
                md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
    except requests.ConnectionError:
        print('Failed to save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        save_image(item)


if __name__ == '__main__':
    groups = [x * 20 for x in range(1, 5)]
    os.chdir('../weibo_ajax/images')    # 提前切换到图片存放目录
    for val in groups:
        main(val)
