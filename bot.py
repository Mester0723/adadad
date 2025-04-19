import telebot, random
from bot_logic import gen_path, gen_emodji, flip_coin, get_class


bot = telebot.TeleBot('7710487723:AAEPjtnQFMpYyuuLGDTRC0F7FthitzN0uSU')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я твой бот Telegram! Напиши /help, чтобы узнать, что я умею.')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, '/hello - поздороваться'
                          '/bye - попрощаться'
                          '/pass - сгенерировать пароль'
                          '/emodji - сгенерировать эмоджи'
                          '/flip - подбросить монетку'
                          '/photo - распознать объект на фото')
    
@bot.message_handler(commands=['hello'])
def hello_message(message):
    bot.reply_to(message, 'Привет!')

@bot.message_handler(commands=['bye'])
def bye_message(message):
    bot.reply_to(message, 'Пока!')

@bot.message_handler(commands=['pass'])
def pass_message(message):
    password = gen_path()
    bot.reply_to(message, f'Ваш пароль: {password}')

@bot.message_handler(commands=['emodji'])
def emodji_message(message):
    emodji = gen_emodji()
    bot.reply_to(message, f'Ваши эмоджи: {emodji}')

@bot.message_handler(commands=['flip'])
def flip_message(message):
    coin = flip_coin()
    flip = random.randint(0, 1)
    if flip == 0:
        bot.reply_to(message, f'Вам выпал: {coin} Орел!')
    else:
        bot.reply_to(message, f'Вам выпал: {coin} Решка!')

@bot.message_handler(commands=['photo'])
def photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, result)

bot.polling()