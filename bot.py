from init import config_create, cwd
from dataclasses import dataclass
import pyrogram
import func as f
import datetime
import rich


Button = pyrogram.types.InlineKeyboardButton
filters = pyrogram.filters
config = config_create()
cache = []


bot = pyrogram.Client(
    session_name = 'bot',
    bot_token = config['bot_token'],
    api_id = config['api_id'],
    api_hash = config['api_hash'],
    workdir = cwd,
)

console = rich.console.Console()
log = console.log


def callback_filter(callback):
    async def func(
        __,
        _,
        query
    ):
        return callback == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(
        func = func,
        data = callback,
    )


@dataclass
class Bot:
    help_message = '''
Я - бот для предложки, как в вк. Пришли сообщение, чтобы предложить его в @example_gmanka_channel

Автор бота - @gmanka. Делаю ботов, 4000 рублей или 50 баксов/евро за бота. Оплата в рублях, долларах, евро и крипте. Писать только по деловым предложениям.

О багах в боте сообщать в @suggest_chat
'''


@dataclass
class Buttons:
    suggest = pyrogram.types.InlineKeyboardMarkup(
        [
            [
                Button(
                    text = 'проверил, предложить пост',
                    callback_data = 'suggest',
                ),
            ],
        ],
    )

    suggested = pyrogram.types.InlineKeyboardMarkup(
        [
            [
                Button(
                    text = 'пост предложен✅',
                    callback_data = 'empty',
                ),
            ],
        ],
    )


@bot.on_message(
    filters.command(
        [
            'help',
            'start',
            'h',
            's'
        ]
    )
)
async def start_command(
    _,
    msg
):
    await msg.reply(
        Bot.help_message
    )


@bot.on_message()
async def forward_to_confirm_channel(
    app,
    msg
):
    if msg.media_group_id:
        now = datetime.datetime.now()
        deadline = now - datetime.timedelta(
            seconds = 3
        )
        if cache:
            for item in cache:
                cached_id, time = item
                if cached_id == msg.media_group_id:
                    return
                if time < deadline:
                    cache.remove(item)
        cache.append((msg.media_group_id, now))

    chat = msg.chat.id

    log(f'forwarding message {msg} from {f.get_username(msg.from_user)} to confirming_chat {config["confirming_chat"]}')

    if msg.media_group_id:
        suggestion = (
            await bot.copy_media_group(
                chat_id = chat,
                from_chat_id = chat,
                message_id = msg.message_id,
                captions = msg.caption,
            )
        )[0]
    else:
        suggestion = await msg.copy(
            chat,
        )

    await suggestion.reply(
        text = 'Проверь этот пост, потому что его нельзя будет отредактировать или удалить',
        quote = True,
        reply_markup = Buttons.suggest
    )

    # text = f'Пост предложен пользователем {msg.from_user.mention()}',


@bot.on_callback_query(
    callback_filter(
        'empty'
    )
)
def answer_empty(
    _,
    cb,
):
    cb.answer()


@bot.on_callback_query(
    callback_filter(
        'suggest'
    )
)
def suggest(
    _,
    cb,
):
    cb.message.edit_reply_markup(
        Buttons.suggested
    )
