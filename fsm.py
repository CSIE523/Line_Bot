from transitions.extensions import GraphMachine
from utils import *
from linebot import LineBotApi, WebhookParser
from dotenv import load_dotenv
from linebot.models import *


load_dotenv()
channel_secret1 = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token1 = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token1)
parser = WebhookParser(channel_secret1)

item_database = []
cost_database = []
list1 = []

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs,):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return text == "你好"


    def is_going_to_expense(self, event):
        text = event.message.text
        return text == "記帳"


    def is_going_to_climate(self, event):
        text = event.message.text
        return text == "天氣狀況"


    def is_going_to_news(self, event):
        text = event.message.text
        return text == "頭條新聞"


    def is_going_to_thingandcost(self, event):
        text = event.message.text
        return text == "輸入項目與金額"

    def is_going_to_storedata(self, event):
        text = event.message.text
        global test
        test = text.split()
        return len(test) == 2 and test[1].isdigit()

    def is_going_to_printtotal(self, event):
        text = event.message.text
        return text == "總消費金額"


    def is_going_to_clear(self, event):
        text = event.message.text
        return text == "清空"


    def is_going_to_north(self, event):
        text = event.message.text
        return text== "北"


    def is_going_to_west(self, event):
        text = event.message.text
        return text == "西" or text == "中"


    def is_going_to_south(self, event):
        text = event.message.text
        return text.lower() == "南"


    def is_going_to_Taipei(self, event):
        text = event.message.text
        return text == "台北" or text == "臺北"


    def is_going_to_NewTaipei(self, event):
        text = event.message.text
        return text == "新北"


    def is_going_to_Taoyuan(self, event):
        text = event.message.text
        return text == "桃園"


    def is_going_to_Taichung(self, event):
        text = event.message.text
        return text == "台中" or text == "臺中"


    def is_going_to_Tainan(self, event):
        text = event.message.text
        return text == "台南" or text == "臺南"


    def is_going_to_Kaohsiung(self, event):
        text = event.message.text
        return text == "高雄"


    def on_enter_start(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='開啟您美好的一天!', text='請輸入或點選服務項目',
                actions=[
                    MessageTemplateAction(label='記帳', text='記帳'),
                    MessageTemplateAction(label='天氣狀況', text='天氣狀況'),
                    MessageTemplateAction(label='頭條新聞', text='頭條新聞')
                ]
                )
            )
        )


    def on_enter_expense(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='您今天記帳了嗎!', text='請輸入或點選服務項目',
                actions=[
                    MessageTemplateAction(label='輸入項目與金額', text='輸入項目與金額'),
                    MessageTemplateAction(label='總消費金額', text='總消費金額'),
                    MessageTemplateAction(label='清空', text='清空')
                ]
                )
            )
        )


    def on_enter_climate(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='直轄市方位選擇', text='請輸入地區方位',
                actions=[
                    MessageTemplateAction(label='北部', text='北'),
                    MessageTemplateAction(label='中部', text='中'),
                    MessageTemplateAction(label='南部', text='南')
                ]
                )
            )
        )


    def on_enter_news(self, event):
        send_text_message(event.reply_token, scrapenews())

        self.go_back()

    def on_enter_thingandcost(self, event):
        send_text_message(event.reply_token, "請輸入您所消費的項目以及金額(ex: 麥當勞 100)")



    def on_enter_storedata(self, event):
        item_database.append(test[0])
        cost_database.append(int(test[1]))
        send_text_message(event.reply_token, "儲存完畢")

        self.go_back()

    def on_enter_printtotal(self, event):
        if not cost_database:
            send_text_message(event.reply_token, "目前您的帳簿是空的")
        else:
            send_text_message(event.reply_token, "目前您總共花了{}元".format(sum(cost_database)))

        self.go_back()

    def on_enter_clear(self, event):
        item_database.clear()
        cost_database.clear()
        send_text_message(event.reply_token, "清除完成!")

        self.go_back()

    def on_enter_north(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='北部地區直轄市選擇', text='請輸入或點選地區',
                actions=[
                    MessageTemplateAction(label='臺北', text='臺北'),
                    MessageTemplateAction(label='新北', text='新北'),
                    MessageTemplateAction(label='桃園', text='桃園')
                ]
                )
            )
        )

    def on_enter_west(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='中部地區直轄市選擇', text='請輸入或點選地區',
                actions=[
                    MessageTemplateAction(label='臺中', text='臺中'),
                ]
                )
            )
        )

    def on_enter_south(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(title='南部地區直轄市選擇', text='請輸入或點選地區',
                actions=[
                    MessageTemplateAction(label='臺南', text='臺南'),
                    MessageTemplateAction(label='高雄', text='高雄'),
                ]
                )
            )
        )

    def on_enter_Taipei(self, event):
        city="臺北市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '近 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                      data[2]['parameter']['parameterName'],
                                                                      data[4]['parameter']['parameterName'],
                                                                      data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    )for data in res
                ]
            )
        ))

        self.go_back()
    def on_enter_NewTaipei(self, event):

        city = "新北市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '近 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                       data[2]['parameter']['parameterName'],
                                                                       data[4]['parameter']['parameterName'],
                                                                       data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    ) for data in res
                ]
            )
        ))

        self.go_back()

        self.go_back()
    def on_enter_Taoyuan(self, event):

        city = "桃園市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '近 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                       data[2]['parameter']['parameterName'],
                                                                       data[4]['parameter']['parameterName'],
                                                                       data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    ) for data in res
                ]
            )
        ))

        self.go_back()
    def on_enter_Taichung(self, event):

        city = "臺中市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '近 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                       data[2]['parameter']['parameterName'],
                                                                       data[4]['parameter']['parameterName'],
                                                                       data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    ) for data in res
                ]
            )
        ))

        self.go_back()
    def on_enter_Tainan(self, event):

        city = "臺南市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '近 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                       data[2]['parameter']['parameterName'],
                                                                       data[4]['parameter']['parameterName'],
                                                                       data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    ) for data in res
                ]
            )
        ))

        self.go_back()
    def on_enter_Kaohsiung(self, event):

        city = "高雄市"
        res = scrapeclimate(city)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text=city + '未來 6 小時天氣預測',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/CA65j4q.png',
                        title='{} ~ {}'.format(res[0][0]['startTime'][5:-3], res[0][0]['endTime'][5:-3]),
                        text='天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}%'.format(data[0]['parameter']['parameterName'],
                                                                       data[2]['parameter']['parameterName'],
                                                                       data[4]['parameter']['parameterName'],
                                                                       data[1]['parameter']['parameterName']),
                        actions=[
                            URIAction(
                                label='詳細內容',
                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    ) for data in res
                ]
            )
        ))

        self.go_back()
