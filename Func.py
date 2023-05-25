# -*- coding: UTF-8 -*-
"""
@Project : doubanmusic 
@File    : Func.py
@IDE     : PyCharm 
@Author  : 爱写屎山的wky
@Email   : 1933658780@qq.com
@Date    : 2023/5/25 20:23 
@Comment : 爬虫相关函数
"""
import time
import csv
import requests
import re
from bs4 import BeautifulSoup


def getUserHome(username):
    user_info_list = []  # 用户信息列表
    home_url = f'https://www.douban.com/search?cat=1005&q={username}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    res_html = requests.get(home_url, headers=headers).text
    soup = BeautifulSoup(res_html, 'lxml')
    user_result_list = soup.find_all(attrs={'class': 'result'})
    user_content_list = soup.find_all(attrs={'class': 'content'})
    for item in range(len(user_result_list)):
        user_data = {'number': item,
                     'id': get_id(user_result_list[item].find('a').get('href')),
                     'name': user_content_list[item].find('a').text,
                     'music_home': get_music_home(get_id(user_result_list[item].find('a').get('href'))),
                     'follows_place': user_content_list[item].find('div', attrs={'class': 'info'}).text.strip()}
        if user_content_list[item].p is not None:
            user_data['info'] = user_content_list[item].p.text
        else:
            user_data['info'] = 'None'
        user_info_list.append(user_data)
    return user_info_list


def get_id(url):
    """
    从url中获取id
    :param url: 需要解析的url
    :return: id
    """
    pattern = r'%2Fpeople%2F(.+)%2F&query='
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def get_music_home(user_id):
    url = f'https://music.douban.com/people/{user_id}/collect'
    return url


def get_music_list(user_id):
    number = 0
    music_all_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    while True:
        url = f'https://music.douban.com/people/{user_id}/collect?start={str(number)}&sort=time&rating=all&filter=all&mode=grid'
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, 'lxml')
        music_all = soup.find(attrs={'class': 'grid-view'})  # 筛选音乐
        music_list = music_all.find_all(attrs={'class': 'item'})  # 单页音乐列表
        if not music_list:
            break
        for item in range(len(music_list)):
            music_dict = {}
            music_dict['album_name'] = music_list[item].find('div', attrs={'class': 'pic'}).find('a').get('title')
            music_dict['album_url'] = music_list[item].find('div', attrs={'class': 'pic'}).find('a').get('href')
            music_dict['album_cover'] = music_list[item].find('div', attrs={'class': 'pic'}).find('a').find('img').get('src')
            music_dict['album_info'] = music_list[item].find('div', attrs={'class': 'info'}).ul.find('li', attrs={'class': 'intro'}).text
            music_dict['signed_time'] = music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'date'}).text
            if music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating5-t'}) or \
                    music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating4-t'}) or \
                    music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating3-t'}) or \
                    music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating2-t'}) or \
                    music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating1-t'}):  # 判断是否评分
                if music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating5-t'}):
                    music_dict['album_rating'] = '5'
                elif music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating4-t'}):
                    music_dict['album_rating'] = '4'
                elif music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating3-t'}):
                    music_dict['album_rating'] = '3'
                elif music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating2-t'}):
                    music_dict['album_rating'] = '2'
                elif music_list[item].find('div', attrs={'class': 'info'}).ul.find('span', attrs={'class': 'rating1-t'}):
                    music_dict['album_rating'] = '1'
            else:
                music_dict['album_rating'] = 'None'
            if not music_list[item].find('div', attrs={'class': 'info'}).ul.find_all('li')[-1].find('span', attrs={'class': 'date'}):
                music_dict['album_comments'] = re.sub(r'\s+', ' ', (music_list[item].find('div', attrs={'class': 'info'}).ul.find_all('li')[-1].text.strip().replace('\n', '')))
            else:
                music_dict['album_comments'] = 'None'
            music_all_list.append(music_dict)
        print(f'正在爬取第{number // 15 + 1}页')
        time.sleep(5)
        number += 15
    return music_all_list


def write_dict_list_to_csv(data, filename):
    # 获取所有可能的键，作为 CSV 文件的表头
    keys = set().union(*data)

    with open(f'./data/{filename}', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()  # 写入表头

        for row in data:
            writer.writerow(row)
