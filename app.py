from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageCarouselColumn, ImageCarouselTemplate

line_bot_api = LineBotApi('c5d4HO2JNGbKKQSSGnu7QiOCf0/+/ROYQUS3taDxc/xSEn68ZN+EiFEgQdtDn4429MrvhKyE1sJ6u8Feu6dG3bOWZfpse/mvsuzGk08Mqtrek0iF+7TUQEMRn5cwbsAHUASgtWu2zdrR9lhgcFas5gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2b1ddbe9c87280e1ac453de1cf0c5ac3')

#這塊APP回應的地方
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#收到使用者傳什麼訊息接收用的
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text #使用者輸入的文字
    
    if mtext == '我要買月餅': #單單一頁的並包含三個按鈕
        sendButton(event)

    elif mtext == '@確認樣板': #這像是會顯示你確定要購買商品並且有是跟否
        sendConfirm(event)

    elif mtext == '景點查詢': #這是有非常多個單頁的旋轉樣板
        sendViewPoint(event)

    elif mtext == '@圖片轉盤': #點選圖片會有文字產生
        sendImgCarousel(event)

    elif mtext == '@我要買豆沙月餅': #當使用者輸入這字串會觸發快速選單(就是下面會有一排按鈕)
        sendMoon(event)

    elif mtext == '@yes': #純粹的文字回復
        sendYes(event)

    elif mtext in ['位置', '實體店面', '地址']: #傳送位置
        sendMap(event)

    elif mtext == '你好':
        sendHi(event)

    elif mtext == '導覽機器人服務':
        sendRobotService(event)


@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)

def sendHi(event): #想要一開始就傳送打招呼跟選擇真人導覽或是機器人導覽
        try:
            message =[ 
                TextSendMessage(
                    text='你好，需要什麼幫助嗎?',
                ),
                TextSendMessage(
                    text='請選擇導覽服務類型',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="真人導覽服務", text="真人導覽服務")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="導覽機器人服務", text="導覽機器人服務")
                            ),
                        ]
                    )
                )
            ]
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendRobotService(event): #當點選到機器人導覽服務的時候會產出五項快速選單
    try:
        message =TextSendMessage(
            text='請選擇要導覽的項目:',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="景點查詢", text="景點查詢")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="遊記查詢", text="遊記查詢")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="交通查詢", text="交通查詢")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="路線查詢", text="路線查詢")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="天氣查詢", text="天氣查詢")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='我要買月餅',
            template=ButtonsTemplate(
                thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/mooncake_01.png',  #顯示的圖片
                title='小美噗豆沙月餅',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='我要+1',
                        text='@我要買豆沙月餅'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='連結網頁',
                        uri='https://www.taipeileechi.com.tw/web/frmProductList.aspx?MenuID=4'
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='回傳訊息',  #按鈕文字
                        #text='@購買披薩',  #顯示文字訊息
                        data='action=buy'  #Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendConfirm(event):  #YES NO 確認樣板
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎？',
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label='是',
                        text='@yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendViewPoint(event):  #景點的轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='景點查詢',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/%E9%99%B3%E5%A4%A9%E4%BE%86%E6%95%85%E5%B1%85.jpg',
                        title='古蹟介紹',
                        text='古蹟介紹',
                        actions=[
                            MessageTemplateAction(
                                label='了解更多',
                                text='了解更多'
                            ),
                            URITemplateAction(
                                label='VR虛擬導覽',
                                uri='https://my-parpertest.web.app/hello/hello.html'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/%E5%8F%B0%E5%8C%97%E9%9C%9E%E6%B5%B7%E5%9F%8E%E9%9A%8D%E5%BB%9F.jpg',
                        title='歷史廟宇',
                        text='歷史廟宇',
                        actions=[
                            MessageTemplateAction(
                                label='了解更多',
                                text='了解更多'
                            ),
                            URITemplateAction(
                                label='VR虛擬導覽',
                                uri='https://my-parpertest.web.app/hello/hello.html'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/%E8%80%81%E9%8C%A6%E6%88%90%E7%87%88%E7%B1%A0%E5%BA%97.jpg',
                        title='特色商行',
                        text='特色商行',
                        actions=[
                            MessageTemplateAction(
                                label='了解更多',
                                text='了解更多'
                            ),
                            URITemplateAction(
                                label='VR虛擬導覽',
                                uri='https://my-parpertest.web.app/hello/hello.html'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/%E5%A4%A7%E7%A8%BB%E5%9F%95%E7%A2%BC%E9%A0%AD.jpg',
                        title='特色景點',
                        text='特色景點',
                        actions=[
                            MessageTemplateAction(
                                label='了解更多',
                                text='了解更多'
                            ),
                            URITemplateAction(
                                label='VR虛擬導覽',
                                uri='https://my-parpertest.web.app/hello/hello.html'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息四',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


# def sendViewPointPhoto(event):
#     try:
#         message = TemplateSendMessage(
#             alt_text='景點查詢',
#             template=ImageCarouselTemplate(
#                 columns=[
#                     ImageCarouselColumn(
#                         image_url='https://example.com/item1.jpg',
#                         action=PostbackAction(
#                         label='postback1',
#                         display_text='postback text1',
#                         data='action=buy&itemid=1'
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         image_url='https://example.com/item2.jpg',
#                         action=PostbackAction(
#                         label='postback2',
#                         display_text='postback text2',
#                         data='action=buy&itemid=2'
#                         )
#                     )
#                 ]
#             )    
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendImgCarousel(event):  #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4QfKuz1.png',
                        action=MessageTemplateAction(
                            label='文字訊息',
                            text='素月餅'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/qaAdBkR.png',
                        action=PostbackTemplateAction(
                            label='回傳訊息',
                            data='action=sell&item=飲料'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendMoon(event):
    try:
        message =[
            TextSendMessage(
                text = '感謝您購買月餅，我們將盡快為您製作。'
            ),
            TextSendMessage(
                text='您還滿意這次的服務嗎？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="非常滿意", text="非常滿意")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="滿意", text="滿意")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="普通", text="普通")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="有待改善", text="有待改善")
                        ),
                    ]
                )
            )
        ] 
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝您的購買，\n我們將盡快寄出商品。',
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata):  #處理Postback
    try:
        #text1 = '感謝您的購買，我們將盡快為您處理。\n(action 的值為 ' + backdata.get('action') + ')'
        #text1 += '\n(可將處理程式寫在此處。)'
        message = TextSendMessage(
            text='您還滿意這次的服務嗎？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="非常滿意", text="非常滿意")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="滿意", text="滿意")
                    ),
                        QuickReplyButton(
                        action=MessageAction(label="普通", text="普通")
                    ),
                        QuickReplyButton(
                        action=MessageAction(label="有待改善", text="有待改善")
                     ),
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendBack_sell(event, backdata):  #處理Postback
    try:
        message = TextSendMessage(  #傳送文字
            text = '點選的是賣 ' + backdata.get('item')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendMap(event):
    try:
        message = LocationSendMessage(
            title='小美噗',
            address='10608台北市大安區忠孝東路三段1號',
            latitude=25.04353847631958,  #緯度
            longitude=121.53769576931987  #經度25.04353847631958, 121.53769576931987
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))  #傳送位置


if __name__ == '__main__':
    app.run()
