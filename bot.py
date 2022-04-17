from init import config_create, cwd
import func as f
import pyrogram
filters = pyrogram.filters

config = config_create()


bot = pyrogram.Client(
    session_name = 'bot',
    bot_token = config['bot_token'],
    api_id = config['api_id'],
    api_hash = config['api_hash'],
    workdir = cwd,
)


@bot.on_message(
    filters.command(
        ('help', 'start')
    )
)
async def start_command(
    app,
    msg
):
    await msg.reply(
        'Hello! Send me any message to suggest it to @example_gmanka_channel'
    )


@bot.on_message()
async def to_admin(app, msg):
    admins = []
    for admin in await app.get_chat_members(
        chat_id = config['channel_id'],
        filter="administrators"
    ):
        if not admin.user.is_bot:
            admins.append(
                admin.user
            )
    username = f.get_username(msg.from_user)
    print(f'forwarding message {msg.message_id} from {username} to admins of channel {config["channel_id"]}')
    for admin in admins:
        admin_name = f.get_username(admin)
        print(f'[blue]trying forwarding[/blue] to {admin_name}')
        try:
            await msg.copy(admin.id)
            print(f'[light_green]success forwarding[/light_green] to {admin_name}')
        except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
            print(f'[red]failed forwarding[/] to {admin_name}, maybe this user didn\'t started bot')


print('bot started')

tg.run()
