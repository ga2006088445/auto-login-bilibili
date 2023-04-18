import requests
import random
import time
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
cookie_file = open(os.path.join(dir_path, 'cookie.txt'), 'r')
_COOKIE = cookie_file.read()
cookie_file.close()

def w_log(msg, filename='log.txt', encoding='utf-8'):
    with open(os.path.join(dir_path, filename), 'a', encoding=encoding) as f:
        f.write(msg + '\n')

def extract_cookies(cookies):
    global _CSRF
    try:
        cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
        _CSRF = cookies['bili_jct']
        return cookies
    except:
        w_log("請使用正確Cookie!")
        exit(9)

# 獲得 各類 B幣值
def get_user_info():
    url = 'https://api.bilibili.com/x/web-interface/nav'
    headers = {'cookie': _COOKIE}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    current_exp = resp_json['data']['level_info']['current_exp']
    coupon_balance = resp_json['data']['wallet']['coupon_balance']
    return {'current_exp': current_exp, 'coupon_balance': coupon_balance}

# 得到每日任務狀態
def get_daily_task_status():
    url = 'https://api.bilibili.com/x/member/web/exp/reward'
    headers = {'cookie': _COOKIE}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    login = resp_json['data']['login']
    watch = resp_json['data']['watch']
    coins = resp_json['data']['coins']
    share = resp_json['data']['share']
    return {'login': login, 'watch': watch, 'coins': coins, 'share': share}


# 排行榜的影片 bvid
def get_rank_videos():
    url = 'https://api.bilibili.com/x/web-interface/ranking'
    headers = {'cookie': _COOKIE}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    videosInfo = resp_json['data']['list']
    bvids = [x['bvid'] for x in videosInfo]
    return {'bvids': bvids}

# 分享影片
def share_video(bvid):
    url = 'https://api.bilibili.com/x/web-interface/share/add'
    headers = {
        'referer': 'https://www.bilibili.com/',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    data = {
        'bvid': bvid,
        'csrf': _CSRF
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        resp_json = response.json()
        if resp_json['code'] == 0:
            return True
    return False

def watch_video(bvid):
    playedTime = random.randint(10, 100)
    url = 'https://api.bilibili.com/x/click-interface/web/heartbeat'
    headers = {
        'referer': 'https://www.bilibili.com/',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    data = {
        'bvid': bvid,
        'played_time': playedTime,
        'csrf': _CSRF
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        resp_json = response.json()
        if resp_json['code'] == 0:
            return True
    return False
        
def get_day_coin():
    url = 'https://api.bilibili.com/x/web-interface/coin/today/exp'
    headers = {'cookie': _COOKIE}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    coins = resp_json['data']
    return {'coins': coins}

def send_coin(bvid):
    coins = get_day_coin()['coins']
    if coins >= 50:
        w_log("不需要投幣, 呼叫錯誤")
        return False

    url = 'https://api.bilibili.com/x/web-interface/coin/add'
    headers = {
        'referer': 'https://www.bilibili.com/',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    data = {
        'bvid': bvid,
        'multiply': 1,
        'select_like': 1,
        'csrf': _CSRF
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        resp_json = response.json()
        if resp_json['code'] == 0:
            return True
    return False

def xlive_sign():
    url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'
    headers = {'cookie': _COOKIE}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        if resp_json['code'] == 0:
            w_log(resp_json['data']['text'])
            return True
        w_log(resp_json['message'])
    return False



# 每日任務
w_log(f'開始每日')
extract_cookies(_COOKIE)
w_log(f'直播簽到')
sign_res = xlive_sign()
w_log(f'直播簽到結果 {sign_res}')

day_status = get_daily_task_status()
video_bvids = get_rank_videos()['bvids']
if day_status['share'] is False:
    w_log(f'需要分享影片')
    video_bvid = random.choice(video_bvids)
    share_res = share_video(video_bvid)
    time.sleep(3)
    w_log(f'分享影片結果 {share_res}')

if day_status['watch'] is False:
    w_log(f'需要觀看影片')
    video_bvid = random.choice(video_bvids)
    watch_res = watch_video(video_bvid)
    time.sleep(3)
    w_log(f'觀看影片結果 {watch_res}')

if day_status['coins'] < 50:
    w_log(f'需要投幣')
    need_number = int(5 - (day_status['coins'] / 10))
    for i in range(need_number):
        video_bvid = random.choice(video_bvids)
        send_coin(video_bvid)
    w_log(f'本次投幣結果 {get_day_coin()}')


day_status_end = get_daily_task_status()
w_log(f'每日進度 {day_status_end}')
