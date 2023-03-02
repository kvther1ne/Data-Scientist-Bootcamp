import telebot
import requests
import time


class rest:

  def __init__(self, link, key):
    self.key = key
    self.link = 'http://www.omdbapi.com/?t=' + link + '&apikey=' + key

  def get(self, link):
    return requests.get(link).json()


token = "6206202622:AAGtKYFLwlrQgZcBi8NYZoO4-HfHJxUk8uI"

bot = telebot.TeleBot(token)
communication = False


@bot.message_handler(commands=['start'])
def start_message(message):
  global communication
  communication = True
  bot.send_message(message.chat.id, "Hello! Send me a movie's name:)")


# Need add comand in bot /stop
@bot.message_handler(commands=['stop'])
def start_message(message):
  if communication:
    bot.send_message(message.chat.id, "Have a good day, bye!")
    communication = False
  else:
    bot.send_message(message.chat.id,
                     "You didn't start communicating with me.")


# Need add comand in bot /help
@bot.message_handler(commands=['help'])
def start_message(message):
  bot.send_message(
    message.chat.id, '\
        commands:\n\
        \t/start - start communicating \n\
        \t/stop  - stop communicating\n\n\
        Send me the title of the movie and I\'ll give you back information about it.'
  )


def generate_message(result) -> str:
  message =  'Title: ' + result['Title'] + '\n' + 'Year: ' + result['Year'] + '\n' + \
  'Rated: ' + result['Rated'] + '\n' + 'Runtime: ' + result['Runtime'] + '\n' + \
  'Genre: ' + result['Genre'] + '\n' + 'Actors: ' + result['Actors'] + '\n' +\
  'Awards: ' + result['Awards'] + '\n' + \
  'BoxOffice: ' + result['BoxOffice'] + '\n' +\
  'Rating: ' + result['imdbRating']
  return message


@bot.message_handler(content_types=["text"])
def answer(message):
  print(communication)
  if communication:
    movie_name = rest(message.text.replace(' ', '+'), 'cbfa76ec')
    result = movie_name.get(movie_name.link)
    # print(result)
    if result['Response'] == 'True':
      bot.send_message(message.chat.id, generate_message(result))
    else:
      bot.send_message(message.chat.id, 'Error: ' + result['Error'])
  else:
    bot.send_message(message.chat.id, 'Enter the /start command to begin.')


while True:
  try:
    bot.polling(none_stop=True)
  except:
    print('Error!')
    time.sleep(5)
