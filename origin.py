'''
这份原稿就直接把Git历史里的搬过来了啊。

不知道bug修好之后这个能不能运行。然后不要忘了在`config.py`里加上password哦！
'''
from requests import Session
from random import random
from json import dump
from csv import DictWriter
from re import search

import config

with Session() as s:
    s.headers.update()
    # 话说一开始在这里卡了好久，因为看到网页里有个`json: true`
    # 就写的是json={...} [Facepalm]
    r = s.post('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do', data={
        'appid': 'card_auth',
        'redirUrl': 'http://sfrzcard.pku.edu.cn/ias/prelogin?sysid=WXXY',
        'userName': config.user_name,
        'password': config.password,
    }).json()
    print(r)
    token = r['token']
    # iaaa是先POST获取token，再把token用GET传给这个神奇的网址
    # 然而漏洞就在于这个GET传参貌似没有为后面步骤起到作用
    # 于是...这个登录流程可谓是“形式主义”
    r = s.get(
        'http://sfrzcard.pku.edu.cn/ias/prelogin?sysid=WXXY',
        params={
            'rand': random(),
            'token': token,
        }
    )
    print(r.text)
    ticket = search('id="ssoticketid" value="(.*?)"', r.text).group(1)
    # ============以下就基本是`main.py`里的内容了============
    r = s.post('https://card.pku.edu.cn/cassyno/index', data={
        'errorcode': 1,
        'continueurl': '',
        'ssoticketid': ticket  # config.user_name
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
    data = []
    i = 1
    while True:
        r = s.post('https://card.pku.edu.cn/Report/GetPersonTrjn', data={
            'sdate': config.start_date,
            'edate': config.end_date,
            'account': account,
            'page': i,
        })
        print(r.text)
        data.extend(r.json()['rows'])
        total = r.json()['total']
        if i >= (total // 15) + (total % 15 > 0):
            break
        i += 1

with open(config.output_file_name+'.json', 'w', encoding='utf-8') as f:
    dump(data, f, ensure_ascii=False, indent=4)

fields = data[0].keys()
with open(config.output_file_name+'.csv', 'w', encoding='utf-8-sig',
          newline='') as f:
    writer = DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for rec in data:
        rec['MERCNAME'] = rec['MERCNAME'].strip()
        rec['TRANNAME'] = rec['TRANNAME'].strip()
        print(rec)
        writer.writerow(rec)
