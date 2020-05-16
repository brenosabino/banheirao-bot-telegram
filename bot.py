#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from config.auth import token
from gtts import gTTS
from pydub import AudioSegment

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    logger.info('Command received')
    # job = context.job
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hi! I'm a bot"
    )


def help(update, context):
    update.message.reply_text('Pra falar algo digite /tts qualquermerda')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def tts(update, context):
    text_to_speech = (' '.join(context.args))
    lang = 'pt-br'
    tts_object = gTTS(text=text_to_speech, lang=lang)
    tts_object.save("tts.mp3")
    logger.info(f'File created with text: {text_to_speech}')
    AudioSegment.from_mp3('tts.mp3').export('result.ogg', format='ogg', codec="libopus")
    logger.info(f'File converted')
    audio_file = "result.ogg"
    context.bot.send_voice(chat_id=update.message.chat_id, voice=open(audio_file, 'rb'))


def main():
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('tts', tts, pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
