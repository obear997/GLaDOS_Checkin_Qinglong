# -*- coding: utf8 -*-
import requests ,os
import json
# 消息推送开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = 'on'
# 填写pushplus的token，不开启则不用填（自己更改）
pushplus_token = '8c01e6a6b64145e9b5d270117227225c'
# 填入glados账号对应cookie
cookie = 'koa:sess=eyJ1c2VySWQiOjkxMDk3LCJfZXhwaXJlIjoxNjY2OTY0ODg1NzAxLCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=X26NOVtI6WoVqt30oV5ebEYGD3k'

def start():
    
    checkin_url = "https://glados.one/api/user/checkin"
    status_url = "https://glados.one/api/user/status"
    origin = "https://glados.one"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
      'token': "glados.network"
    }

    checkin = requests.post(checkin_url, headers = {
      'cookie': cookie ,
      'origin':origin,
      'user-agent':useragent,
      'content-type':'application/json;charset=UTF-8'
    }, data = json.dumps(payload))

    state =  requests.get(status_url, headers = {
      'cookie': cookie ,
      'user-agent':useragent
    })

    if sever == 'off':
      print('消息推送开关未打开，不推送签到结果')
     
    else:
      # pushplus
      if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays'].split('.')[0]
        print(time)

        requests.get('http://www.pushplus.plus/send?token=' + pushplus_token +'&title=GLaDOS自动签到&content=' + '您的Glasod账号 '+time+' 天后到期，' + mess)

        print("签到任务执行成功，" + '您的Glasod账号 '+ time + ' 天后到期，' + mess )
        
        print('pushplus送消息成功')

      else:
        requests.get('http://www.pushplus.plus/send?token=' + pushplus_token +'&title=GLaDOS自动签到&content=cookie过期')

def main_handler(event, context):
  return start()

if __name__ == '__main__':
  start()