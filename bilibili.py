import requests
import random
import time
import os
import argparse

def w_log(msg, filename='log.txt', encoding='utf-8'):
    print(msg)
    if args.logfile is True:
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
    headers = {
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    current_exp = resp_json['data']['level_info']['current_exp']
    coupon_balance = resp_json['data']['wallet']['coupon_balance']
    return {'current_exp': current_exp, 'coupon_balance': coupon_balance}

# 得到每日任務狀態
def get_daily_task_status():
    url = 'https://api.bilibili.com/x/member/web/exp/reward'
    headers = {
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    w_log(f'[Debug] 每日任務狀態 : {resp_json}')

    login = resp_json['data']['login']
    watch = resp_json['data']['watch']
    coins = resp_json['data']['coins']
    share = resp_json['data']['share']
    return {'login': login, 'watch': watch, 'coins': coins, 'share': share}


# 排行榜的影片 bvid
def get_rank_videos():
    url = 'https://api.bilibili.com/x/web-interface/ranking'
    headers = {
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
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
    headers = {
        'cookie': _COOKIE,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
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
    headers = {
        'cookie': _COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        if resp_json['code'] == 0:
            w_log(resp_json['data']['text'])
            return True
        if resp_json['code'] == 1011040:
            w_log(resp_json['message'])
            return True
        w_log(resp_json['message'])
    return False


# 解析參數
parser = argparse.ArgumentParser(description="Bilibili每日任務")
# 添加參數
# 是否要把 Log 同步寫入檔案中
parser.add_argument('--logfile', dest='logfile', action='store_true', help='啟用日誌檔案寫入')
parser.add_argument('--no-logfile', dest='logfile', action='store_false', help='停用日誌檔案寫入')
parser.set_defaults(logfile=False)

# 是否自動直播簽到
parser.add_argument('--liveSign', dest='liveSign', action='store_true', help='啟用自動直播簽到')
parser.add_argument('--no-liveSign', dest='liveSign', action='store_false', help='停用自動直播簽到')
parser.set_defaults(liveSign=True)

# 是否分享影片
parser.add_argument('--shareVideo', dest='shareVideo', action='store_true', help='啟用影片分享')
parser.add_argument('--no-shareVideo', dest='shareVideo', action='store_false', help='停用影片分享')
parser.set_defaults(shareVideo=True)

# 是否瀏覽影片
parser.add_argument('--watchVideo', dest='watchVideo', action='store_true', help='啟用影片瀏覽')
parser.add_argument('--no-watchVideo', dest='watchVideo', action='store_false', help='停用影片瀏覽')
parser.set_defaults(watchVideo=True)

# 是否投幣
parser.add_argument('--coins', dest='coins', action='store_true', help='啟用投幣')
parser.add_argument('--no-coins', dest='coins', action='store_false', help='停用投幣')
parser.set_defaults(coins=True)

# 添加 Cookie 文件路徑參數
parser.add_argument('--cookieFile', type=str, required=True, help='指定 cookie.txt 文件的絕對路徑')

# 解析參數
args = parser.parse_args()

# 使用參數
w_log(f"接收到的啟動參數為: {args}")

# 每日任務
w_log(f'開始 bilibili 每日任務')


w_log(f'讀取 Cookie')
dir_path = os.path.dirname(os.path.abspath(__file__))
cookie_file = open(os.path.join(dir_path, args.cookieFile), 'r')
_COOKIE = cookie_file.read()
cookie_file.close()
w_log(f'讀取 Cookie 完成')

w_log(f'檢查 Cookie')
extract_cookies(_COOKIE)
w_log(f'檢查 Cookie 完成')

day_status = get_daily_task_status()
w_log(f'開始前每日進度: {day_status}')

if args.liveSign is False:
    w_log(f'已禁用直播簽到')
else:
    w_log(f'直播簽到')
    sign_res = xlive_sign()
    w_log(f'直播簽到結果: {sign_res}')

video_bvids = get_rank_videos()['bvids']

# 每日分享影片
if args.shareVideo is False:
    w_log(f'已禁用分享影片')
else:
    if day_status['share'] is True:
        w_log(f'今日已分享影片')
    else:
        w_log(f'需要分享影片')
        video_bvid = random.choice(video_bvids)
        share_res = share_video(video_bvid)
        time.sleep(3)
        w_log(f'分享影片結果: {share_res}')

# 每日觀看影片
if args.watchVideo is False:
    w_log(f'已禁用觀看影片')
else:
    if day_status['watch'] is True:
        w_log(f'今日已觀看影片')    
    else:
        w_log(f'需要觀看影片')
        video_bvid = random.choice(video_bvids)
        watch_res = watch_video(video_bvid)
        time.sleep(3)
        w_log(f'觀看影片結果: {watch_res}')

# 每日投幣
if args.coins is False:
    w_log(f'已禁用投幣')
else:
    if day_status['coins'] >= 50:
        w_log(f'今日已投幣至上限 (50)')
    else:
        w_log(f'目前投幣進度, 需要投幣: {day_status["coins"]}')
        need_number = int(5 - (day_status['coins'] / 10))
        for i in range(need_number):
            video_bvid = random.choice(video_bvids)
            send_coin(video_bvid)
        w_log(f'本次投幣結果: {get_day_coin()}')

day_status_end = get_daily_task_status()
w_log(f'執行完成 進度為: {day_status_end}')
