import os
import requests
import json
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from bs4 import BeautifulSoup
from datetime import datetime

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
token = os.getenv("TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def scrapenews():
    response = requests.get("https://www.ettoday.net/news/focus/%E9%A6%96%E9%A0%81/%E9%A0%AD%E6%A2%9D/")
    soup = BeautifulSoup(response.content, "html.parser")
    sel = soup.select("div.part_list_3 a")
    content = ""
    for i in range(3):
        content += "第{}則:".format(i+1)+sel[i]["title"]+"\n"+"詳細內容請洽:"+"https://www.ettoday.net/"+sel[i]["href"]+"\n\n\n"
    return content

def scrapeclimate(region):
    time = datetime.now()
    if time.hour >= 0 and time.hour < 6:
        mode=0
    elif time.hour >= 6 and time.hour < 18:
        mode=1
    else:
        mode=2
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(region)
    Data = requests.get(url)
    Data = (json.loads(Data.text, encoding='utf-8'))['records']['location'][0]['weatherElement']
    res = [[]]
    for i in Data:
        res[0].append(i['time'][mode])
    return res

