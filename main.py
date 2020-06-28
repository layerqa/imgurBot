import json
import pyimgur
import telebot
import requests

with open('config.json', 'r') as configFile:
    config = json.loads(configFile.read())

bot = telebot.TeleBot(token=config['botToken'])
imgurInit = pyimgur.Imgur(client_id=config['userId'])

@bot.message_handler(content_types=['photo'])
def photoMessage(message):
    photoUrl = bot.get_file_url(file_id=message.photo[0].file_id)
    photo = downloadPhoto(photoId=message.photo[0].file_id, photoUrl=photoUrl)
    bot.reply_to(message=message, text=photo['photoUrl'])


def downloadPhoto(photoId, photoUrl):
    photo = requests.get(url=photoUrl)
    with open(f'images/{photoId}.png', 'wb') as photoFile:
        photoFile.write(photo.content)
        return uploadPhoto(photoPath=f'images/{photoId}.png')


def uploadPhoto(photoPath):
    imgurUpload = imgurInit.upload_image(path=photoPath)
    return {
        'photoUrl': imgurUpload.link,
        'photoSize': imgurUpload.size,
        'photoType': imgurUpload.type
    }

bot.polling(none_stop=True)