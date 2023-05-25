# -*- coding: UTF-8 -*-
"""
@Project : doubanmusic 
@File    : DouBanMusic.py
@IDE     : PyCharm 
@Author  : 爱写屎山的wky
@Email   : 1933658780@qq.com
@Date    : 2023/5/25 20:21 
@Comment : 爬取需求用户的豆瓣音乐榜单
"""
import Func

if __name__ == '__main__':
    user_all = str(input('请输入要爬取已听音乐信息的用户名（最好精确一点）：'))
    user_list = Func.getUserHome(user_all)
    for user in user_list:
        print(user)
    user = user_list[int(input('请输入要爬取的用户序号：'))]
    music_list = Func.get_music_list(user['id'])
    print(f'共有{len(music_list)}首歌曲')
    # 写入csv文件
    username = user['name']
    Func.write_dict_list_to_csv(music_list, f'{username}的已听音乐列表.csv')
    print('爬取完成！')
