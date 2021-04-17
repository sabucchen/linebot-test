from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction 

line_bot_api = LineBotApi('c5d4HO2JNGbKKQSSGnu7QiOCf0/+/ROYQUS3taDxc/xSEn68ZN+EiFEgQdtDn4429MrvhKyE1sJ6u8Feu6dG3bOWZfpse/mvsuzGk08Mqtrek0iF+7TUQEMRn5cwbsAHUASgtWu2zdrR9lhgcFas5gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2b1ddbe9c87280e1ac453de1cf0c5ac3')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    
    if mtext == '@按鈕樣板':
        sendButton(event)

    elif mtext == '@確認樣板':
        sendConfirm(event)

    elif mtext == '@轉盤樣板':
        sendCarousel(event)

    elif mtext == '@圖片轉盤':
        sendImgCarousel(event)

    elif mtext == '@我要買豆沙月餅':
        sendMoon(event)

    elif mtext == '@yes':
        sendYes(event)

    elif mtext in ['位置', '實體店面', '地址']:
        sendMap(event)


@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)

def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
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

def sendConfirm(event):  #確認樣板
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

def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/sabucchen/pic/main/mooncake_02.png',
                        title='小美噗素豆沙月餅',
                        text='奶素',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='素月餅'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri='https://www.taipeileechi.com.tw/'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taipeileechi.com.tw/ProductCategory/ProductUnit20140606193619.jpg',
                        title='這是樣板二',
                        text='第二個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息二',
                                text='葷月餅'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri='https://www.taipeileechi.com.tw/web/frmProductDetail.aspx?MenuID=4&ProductID=20'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
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
        message = TextSendMessage(
            text = '感謝您購買月餅，我們將盡快為您製作。'
        )
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
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


if __name__ == '__main__':
    app.run()
