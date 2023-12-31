import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import prettytable as pt


from pyairtable import Api

AIRTABLE_KEY = os.environ.get('AIRTABLE_KEY')
TELEGRAM_KEY = os.environ.get('TELEGRAM_KEY')
AIRTABLE_APP = os.environ.get('AIRTABLE_APP')
AIRTABLE_TABLE = os.environ.get('AIRTABLE_TABLE')
# stats - general stats by last played games
# top 5 played games. Rows: game, most wins, last played
# stats recent
# stats player
# stats <game> - stats by game

# last - show last 5 games

# specific to root commands
#
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('answering stats')

    api = Api(AIRTABLE_KEY)
    game_sessions_table = api.table(AIRTABLE_APP, AIRTABLE_TABLE)

    table = pt.PrettyTable(['Game', 'Players', 'Won'])
    table.align['Name (from Game)'] = 'l'
    table.align['Name (from Players)'] = 'r'
    table.align['Name (from Won)'] = 'r'

    for record in game_sessions_table.all(max_records=10, sort=['-Date']):
        table.add_row([record["fields"]['Name (from Game)'][0], '\n'.join(record["fields"]['Name (from Players)']), record["fields"]['Name (from Won)'][0]])

    await update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
    # or use markdown
    # await update.message.reply_text(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_KEY).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


if __name__ == '__main__':
    main()
