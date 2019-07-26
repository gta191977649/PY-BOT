import time

from telethon import TelegramClient, events
import pyowm


# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 752685
api_hash = '5fa040066921594f31606e050d73572d'

# fill in your own details here
phone = '+610405574088'
session_file = '.session'  # use your username if unsure
password = ''  # if you have two-step verification enabled

# content of the automatic reply
message = "Sparrow Agent (消失モード): \n\"void 消失了... 可能死了\"\n[你可以尝试以下操作]:\n1.卖萌\n2.天气预报\n3.转告void (自动发邮件给他)\n或者无视\nYour Options(Number only)->"

owm = pyowm.OWM('d2d6d27c4cbb63a2531d5a7348011508')  # You MUST provide a valid API key

hana_userid = 775246270
if __name__ == '__main__':
    def moe():
        return '=w='
    def weather():
        observation = owm.weather_at_place('Sydney,AU')
        w = observation.get_weather()
        temp = w.get_temperature('celsius')
        humidity = w.get_humidity()
        status = w.get_detailed_status()   
        return "Sydney: 天气:{} 温度:{}° 湿度:{}".format(status,temp['temp'],humidity)
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        #if event.is_private:  # only auto-reply to private chats
        from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
        if not from_.bot:  # don't auto-reply to bots
            msg =  event.message.message
            chan = await client.get_entity(event.message.from_id) #775246270
            if event.message.from_id == hana_userid: #检测Hana
                print("!!!!"+chan.first_name+"!!!!")
            else:
                print(chan.first_name)

            print(time.asctime(), '接收到对话',msg)  # optionally log time and message
            # time.sleep(1)
            if msg == '1':
                await event.respond(moe())
            elif msg == '2':
                await event.respond(weather())
            elif msg == '3':
                await event.respond('转告void -> OK')
            else:
                if event.message.from_id == hana_userid: #检测Hana
                    await event.respond(message+"\n Catch: Hana, Response:🧡")
                else:
                    await event.respond(message)

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone, password)
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')

    