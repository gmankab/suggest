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


blacklist = []


console = rich.console.Console()
log = console.log


def callback_filter(*got_callback):
    async def func(
        __,
        _,
        target_callback
    ):
        for i in got_callback:
            if i in target_callback.data:
                return True
        # return target_callback.data in got_callback
        return False

    return filters.create(
        func = func,
        data = got_callback,
    )


async def forward(
    msg,
    target,
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
        return (
            await bot.copy_media_group(
                chat_id = target,
                from_chat_id = msg.chat.id,
                message_id = msg.message_id,
                captions = msg.caption,
            )
        )[0]
    else:
        return await msg.copy(
            target,
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
                    text = 'проверил, отправить',
                    callback_data = 'suggest',
                ),
            ],
        ],
    )
    publish = pyrogram.types.InlineKeyboardMarkup(
        [
            [
                Button(
                    text = 'опубликовать',
                    callback_data = 'publish',
                ),
                Button(
                    text = '↓забанить↓',
                    callback_data = 'open_ban_menu',
                )
            ],
        ],
    )
    ban_menu = pyrogram.types.InlineKeyboardMarkup(
        [
            [
                Button(
                    text = '↑скрыть меню↑',
                    callback_data = 'close_ban_menu',
                )
            ], [
                Button(
                    text = 'забанить навсегда',
                    callback_data = 'ban ever',
                )
            ], [
                Button(
                    text = 'забанить на год',
                    callback_data = 'ban year',
                )
            ], [
                Button(
                    text = 'забанить на месяц',
                    callback_data = 'ban month',
                )
            ], [
                Button(
                    text = 'забанить на неделю',
                    callback_data = 'ban week',
                )
            ], [
                Button(
                    text = 'забанить на 30 секунд',
                    callback_data = 'ban 30_sec',
                )
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
async def on_message(
    app,
    msg
):
    chat = msg.chat.id
    if chat in blacklist:
        return
    log(f'forwarding message {msg} from {f.get_username(msg.from_user)} to confirming_chat {config["confirming_chat"]}')

    await (
        await forward(
            msg,
            chat,
        )
    ).reply(
        text = 'Проверь этот пост, потому что его нельзя будет отредактировать или удалить',
        quote = True,
        reply_markup = Buttons.suggest
    )


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
        'publish'
    )
)
async def publish(
    _,
    cb,
):
    await cb.message.edit(
        text = f'✅\nпредложил {cb.message.entities[0].user.mention()}\nопубликовал {cb.from_user.mention()}'
    )
    await forward(
        msg = cb.message.reply_to_message,
        target = config['main_chat'],
    )


@bot.on_callback_query(
    callback_filter(
        'suggest'
    )
)
async def suggest(
    _,
    cb,
):
    await cb.message.edit(
        text = '✅\nПост отправлен\nЯ пришлю тебе уведомление, когда его опубликуют, или отклонят'
    )

    await (
        await forward(
        msg = cb.message.reply_to_message,
        target = config['confirming_chat'],
        )
    ).reply(
        text = f'предложил {cb.from_user.mention()}',
        quote = True,
        reply_markup = Buttons.publish,
)


def main():
    global blacklist
    bot.start()
    blacklist = list(
        bot.get_chat(
            id
        ).id for id in (
            config['confirming_chat'],
            config['main_chat']
        )
    )
    pyrogram.idle()
