import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def weather(bot, update, days):
    page = requests.get("https://weather.com/fa-IR/weather/tenday/l/IRXX0018:1:IR")
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    trs = list(table.children)[0:days]
    for tr in trs:
        tags = tr.find_all('span')
        text = 'تاریخ: ' + tags[0].text + "...." + tags[1].text
        text += '\n'
        text += 'وضعیت: ' + tags[2].text
        text += '\n'
        text += 'دمای هوا: ' + tags[3].text + '/' + tags[5].text
        text += '\n'
        text += 'رطوبت هوا: ' + tags[11].text
        bot.send_message(update.message.chat_id, text=text)


def how_many_day(bot, update):
    keyboard = [[str(counter) for counter in range(1, 6)],
                [str(counter) for counter in range(6, 11)],
                ['منو اصلی']]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='تا چند روز آینده را می خواهید:', reply_markup=reply_markup)


def currency(bot, update, str):
    page = requests.get("https://www.iranjib.ir/showgroup/23/realtime_price/")
    soup = BeautifulSoup(page.content, 'html.parser')
    if str == 'ارز دیجیتال':
        table = soup.find_all('table')[10]
        array = [2, 4, 6, 8]
        text = 'نرخ لحظه ای ارز دیجیتالا:\n\n'
    else:
        table = soup.find_all('table')[7]
        array = [2, 4]
        text = 'میانگین قیمت ارز در صرافی ها:\n\n'

    trs = table.find_all('tr')
    for i in array:
        tr = trs[i]
        tds = tr.find_all('td')
        text += tds[2].text + ':\n'
        text += 'شاخص: ' + tds[3].text
        text += '\n'
        text += ' تغییرات: ' + tds[4].text
        text += '\n'
        text += ' بیشترین قیمت: ' + tds[5].text
        text += '\n'
        text += ' کمترین قیمت: ' + tds[6].text
        text += '\n\n'
    bot.send_message(update.message.chat_id, text=text)


def which_currency(bot, update):
    keyboard = [['ارز دیجیتال', 'دلا و یورو'],
                ['منو اصلی']]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='ارز مورد نظر را انتخاب کنید:', reply_markup=reply_markup)


def news(bot, update, st):
    if st == 'سیاسی':
        page = requests.get("https://www.bartarinha.ir/fa/list/20/24")
    elif st == 'ورزشی':
        page = requests.get("https://www.bartarinha.ir/fa/athletic")
    elif st == 'فرهنگی':
      page = requests.get("https://www.bartarinha.ir/fa/list/20/55")
    elif st == 'اقتصادی':
        page = requests.get("https://www.bartarinha.ir/fa/list/20/25")
    elif st == 'اجتماعی':
        page = requests.get("https://www.bartarinha.ir/fa/list/20/54")
    else:
        page = requests.get("https://www.bartarinha.ir/fa/list/20/57")
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(class_='service_content')
    titles = content.find_all(class_='Htag')[0:5]
    news = content.find_all('div', class_='lead2')[0:5]
    i = 0
    text = ''
    for title in titles:
        text += (str(i+1) + '.' + title.find('a').text.strip() + ': \n')
        text += news[i].text
        text += '\n\n\n'
        i += 1
    bot.send_message(update.message.chat_id, text=text)


def which_news(bot, update):
    keyboard = [['سیاسی', 'ورزشی', 'فرهنگی'], ['اقتصادی', 'اجتماعی', 'حوادث'],['منو اصلی']]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='نوع خبرهای مورد نظر را انتخاب کنید:', reply_markup=reply_markup)


def calendar(bot, update):
    page = requests.get("https://www.time.ir")
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all('span', class_='show title')[:3]
    dates = soup.find_all('span', class_='show date')[:3]
    numerals = soup.find_all('span', class_='show numeral')[:3]
    i = 0
    text = ''
    for title in titles:
        text += title.text + ': \n'
        text += dates[i].text + '\n'
        text += numerals[i].text + '\n'
        text += '\n\n'
        i += 1
    bot.send_message(update.message.chat_id, text=text)


def start(bot, update):
    keyboard = [['آب و هوا تهران', 'قیمت ارز'],
                ['اخبار روز', 'تقویم'],
                ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='گزینه مورد نظر را انتخاب کنید:', reply_markup=reply_markup)


def answer(bot, update):
    text = update.message.text
    if text == 'قیمت ارز':
        which_currency(bot, update)
    elif text == 'آب و هوا تهران':
        how_many_day(bot, update)
    elif text == 'اخبار روز':
        which_news(bot, update)
    elif text == 'تقویم':
        calendar(bot, update)
    elif text == 'منو اصلی':
        start(bot, update)
    elif text in ['سیاسی', 'ورزشی', 'فرهنگی', 'اقتصادی', 'اجتماعی', 'حوادث']:
        news(bot, update, text)
    elif text in ['ارز دیجیتال', 'دلا و یورو']:
        currency(bot, update, text)
    elif text.isdigit():
        weather(bot, update, int(text))
    else:
        bot.send_message(update.message.chat_id, text='درخواست نامعتبر است!')


updater = Updater('806434415:AAE5kxNqt1eA1Hfgu43MgIwUm64Q9YmNL7w')
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.text, answer))
updater.start_polling()
updater.idle()
