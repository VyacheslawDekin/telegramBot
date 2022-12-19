from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup  #Объект InlineKeyboardButton представляет одну кнопку встроенной клавиатуры
from telegram.ext import Updater
from telegram.ext import CommandHandler  #обработчик, который прослушивает сообщения с командами
from telegram.ext import MessageHandler  #Обработчки, который прослушивает обычные тестовые сообщения
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters  #Фильтры типа сообщения. Содержит ряд так фильтров, которые фильтруют входящие сообщения по тексту, изображениям, обновлениям статуса и т.д.
from telegram.ext.callbackcontext import CallbackContext

from bot.settings import TG_TOKEN


def start(update: Update, context: CallbackContext) -> None:
    """
    Обработчик сообщений-комманд отправленных боту

    Keyword arguments:
    update -- Объект связанный с экземпляром Update который присылает и отправляет все сообщения
    context -- Объект связанный с контекстом обработанного сообщения CallbackContext
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm bot!"
    )

    reply_markup = InlineKeyboardMarkup(build_menu(buttons=button_list, n_cols=2))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Все команды',
        reply_markup=reply_markup
    )


def do_help(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды '/help' отправленных боту

    Keyword arguments:
    update -- Объект связанный с экземпляром Update который присылает и отправляет все сообщения
    context -- Объект связанный с контекстом обработанного сообщения CallbackContext
    """

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="help"
    )


def echo(update: Update, context: CallbackContext) -> None:
    """
    Обработчик текстовых сообщений отправленных боту

    Keyword arguments:
    update -- Объект связанный с экземпляром Update который присылает и отправляет все сообщения
    context -- Объект связанный с контекстом обработанного сообщения
    """

    text = ''.join(['ECHO: ', update.message.text])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def caps(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /caps с аргументами (например: /caps any args). Будут в контексте в виде списка ['any', 'args'], разделенного пробелами

    Keyword arguments:
    update -- Объект связанный с экземпляром Update который присылает и отправляет все сообщения
    context -- Объект связанный с контекстом обработанного сообщения
    """

    # Если в команде нет аргументов
    if not context.args:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='No command argument. Send: /caps argument'
        )
        return

    text_caps = ' '.join(context.args, ).upper()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )


button_list = [
    InlineKeyboardButton("Команда возврата имени", callback_data='send_fullname'),
    InlineKeyboardButton("Команда отправки картинки", callback_data='send_picture'),
    InlineKeyboardButton("Команда отправки gif", callback_data='send_gif'),
    InlineKeyboardButton("Команда отмены рисовки кнопок", callback_data='cancel_command'),
]


def build_menu(buttons: list, n_cols: InlineKeyboardButton, header_buttons=None, footer_buttons=None) -> list:
    """
    Метод формирования меню со списком кнопок

    Keyword arguments:
    buttons -- Список команд для вывода пользователю
    n_cols -- Количество колонок для вывода команд
    header_buttons - Команды, которые необходимо добавить перед основными командами
    footer_buttons - Команды, которые необходимо добавить после основных команд
    """

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])

    return menu


def button(update: Update, context: CallbackContext) -> None:
    """
    Функция обработки нажатия команды

    Keyword arguments:
    update -- Объект связанный с экземпляром Update который присылает и отправляет все сообщения
    context -- Объект связанный с контекстом обработанного сообщения
    """

    query = update.callback_query
    variant = query.data
    query.answer()

    match variant:
        case 'send_fullname':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=update.effective_chat.full_name
            )
        case 'send_picture':
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=open('/Users/vyacheslav_dekin/IdeaProjects/Python3/telegramBot/picture.jpeg', 'rb')
            )
        case 'send_gif':
            context.bot.send_animation(
                chat_id=update.effective_chat.id,
                animation=open('/Users/vyacheslav_dekin/IdeaProjects/Python3/telegramBot/gif.gif', 'rb')
            )
        case 'cancel_command':
            query.edit_message_text(text='Кнопки убраны')


def main() -> None:
    """
    Класс Updater постоянно слушает сервер Telegram, получает новые сообщения и передает их классу Dispatcher.
    Если создать объект Updater, то он автоматически создаст Dispatcher.
    У экземпляра Dispatcher, есть контекст context, который, при регистрации любого обработчика сообщений
    передается в функцию обратного вызова этого обработчика (в нее так же передается updater).
    Каждый обработчик является экземпляром подкласса класса telegram.ext.Handler
    """

    updater = Updater(token=TG_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)  #Если увидит команду '/start', то вызовет функцию start(). Имя функции может быть любым
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)  #Если будет текстовое сообщение и НЕ команда (~Filters.command), то вызовет функцию echo()
    caps_handler = CommandHandler('caps', caps)  # Если увидит команду '/caps', то вызовет функцию caps()
    button_handler = CallbackQueryHandler(button)

    # Добавление обработчиков в 'dispatcher'
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(button_handler)

    updater.start_polling()  #говорим экземпляру 'Updater' слушать сервер Telegram
    updater.idle()  #Обработчик остановки через комбинацию клавиш 'Ctrl+C'


if __name__ == '__main__':
    main()
