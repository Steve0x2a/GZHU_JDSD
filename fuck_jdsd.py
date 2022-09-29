import requests
import json
import random
import time
import os
from loguru import logger


'''
下方填写key 需抓包  key在更换微信登录后会改变 具体有效期尚未可知
'''
key =  str(os.environ['KEY'])
session = requests.session()
headers = {
  'Host': 'jdsd.gzhu.edu.cn',
  'Accept': '*/*',
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000233) NetType/WIFI Language/en',
  'Referer': 'https://servicewechat.com/wxb78a5743a9eed5bf/15/page-frame.html',
  'Accept-Language': 'en-us'
}
session.headers = headers
url = "https://jdsd.gzhu.edu.cn/coctl_gzhu/index_wx.php"
p= str(os.environ['PUSHPLUS'])


def get_info():
    #获取个人信息 name:名字 today:今日获得积分 total:总积分
    flag = False
    info_data = {
        'route':'user_info',
        'key':key
    }
    res = session.post(url,data = info_data).json()
    info = {}
    if res['status'] == 1:
        flag = True
        info['name'] = res['re']['user_name']
        info['today'] = res['re']['per_day_credits']
        info['total'] = res['re']['credits']
    return (flag, info)


def signin():
    #签到
    signin_data = {
        'route':'signin',
        'key':key
    }
    res = session.post(url,data = signin_data).json()


def train():
    #每日一题函数, 可以直接获取每日一题题目编号, 构造编号和"1"的数组发送即可完成每日一题
    get_id_data = {
        'route':'train_list_get',
        'diff' : '0',
        'key' : key
    }
    question = session.post(url,data = get_id_data).json()
    ans = []
    for i in question['re']['question_bag']:
        ans.append([i['num'],"1"])
    train_id = question['re']['train_id']
    train_data = {
        'route':'train_finish',
        'train_id':train_id,
        'train_result' : json.dumps(ans),
        'key':key
    }
    res = session.post(url,data = train_data).json()
    if res['status'] == 1:
        return True
    else:
        return False


def read():
    #阅读函数 type从1到5 开始先发送一个开始的数据包, 结束把addtime换成91再发一次
    read_data = {
    'route' : 'classic_time',
        'addtime' : 0,
        'type':1,
        'key' : key
    }

    for i in range(1,6):
        read_data['type']=i
        read_data['addtime'] = 0
        begin = session.post(url, data = read_data)
        read_data['addtime'] = 91
        end = session.post(url, data = read_data)


def vs():
    '''
    '朴实无华的匹配函数, 先变换counter找到对手, 后150秒内每隔一秒发送心跳包
    '利用了一个bug, 在比赛结束后若继续发送心跳包, 会直接获得段位分和积分
    '但是段位分无上限, 容易造成段位分过高
    '这里判定了开始加分后, 会只执行五次加分操作
    '''
    print('即将开始匹配 需要花费一定时间 请耐心等待')
    vs_find_data = {
        'route':'get_counterpart',
        'key':key,
        'counter':0,
        'find_type':0
    }
    add = 0
    while(1):
        i = 0
        vs_find_data['counter'] = i
        res = session.post(url,data = vs_find_data).json()
        if res['status'] == 1:
            game_key = res['question_bag']['gaming_key']
            break
        i += 1
        if i > 10:
            i = 0
    question_num = get_question_num(res)
    alive_data = {
        'route':'ask_opponent_score',
        'key':key,
        'gaming_key':game_key
    }
    for i in range(150):
        time.sleep(1)
        alive_res = session.post(url,alive_data)
        if alive_res.json()['status'] == 2:
            add += 1
        if add >= 5:
            break




'''
下面两个函数是获取题目num和对应答案和提交匹配时答案的接口 但基本用不到 因为我们根本不需要提交...

'''
def get_question_num(res):
    #res是获取匹配成功后的json
    question = []
    for i in res['question_bag']['question_arr']:
        question.append(i['num'])
    return question

def get_answer(num):
    get_answer_data={
        'route':'ascertain_answer',
        'key':key,
        'gaming_key':'777777',
        'question_id':'.coctl',
        'answer_id':'q',
        'question_num':num,
        'current_time':'0'
    }
    ans_data = session.post(url,data=get_answer_data).json()
    return ans_data['test_item2']['answer']

def post_answer(num,answer):
    post_answer_data={
        'route':'ascertain_answer',
        'key':key,
        'gaming_key':'777777',
        'question_id':'.coctl',
        'answer_id':answer,
        'question_num':num,
        'current_time':str(random.randint(100,180))
    }
    ans_data = session.post(url,data=post_answer_data).json()



def bark(flag,message = None):
    #接入bark通知 可以修改bark_url推送到自己手机(iOS only)
    bark_url = ''
    global text1,text2
    if flag:
        text1 = '{}刷分成功/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '返回信息:{}'.format(message)
    else:
        text1 = '{}刷分失败了快去看看/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '快看看'
    requests.post(bark_url+'/'+text1+text2)


if __name__ == '__main__':
    try:
        #先验证登录
        flag, info = get_info()
        if not flag:
            raise Exception("登录失败 请验证key")
            data = {"token": '36e93ed9a2e44e478b9fe30aeff66b81', "title": '经典诵读登录失败', "content": ' '}
            url = "http://www.pushplus.plus/send/"
            logger.info(requests.post(url, data=data).text)
        print("{}同学您好,您目前的积分为:{}".format(info['name'],info['total']))
        #签到+2
        signin()
        print('已完成签到')
        #进行每日一题
        for i in range(15):
            train()
        print('已完成每日一题')
        #阅读一哈
        read()
        print('已完成阅读')
        #匹配一哈
        vs()
        print('已完成匹配')
        #返回
        flag, info = get_info()
        string = "今日获得:{} 总积分:{}".format(info['today'],info['total'])
        print(string)
        #通知 需要填入bark_url
        #bark(1,message = string)
    except Exception as e:
        print(e)
        #bark(0,message = e)
    if string[0] =="今":
        data = {"token": p, "title": '经典诵读', "content": string}
        url = "http://www.pushplus.plus/send/"
        logger.info(requests.post(url, data=data).text)
    else:
        data = {"token": p, "title": '经典诵读匹配失败', "content": " "}
        url = "http://www.pushplus.plus/send/"
        logger.info(requests.post(url, data=data).text)
        


    
