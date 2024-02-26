import interactions
from interactions import slash_command, subcommand, OptionType, slash_option
from decouple import config

BOT_TOKEN = config('BOT_TOKEN1')
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1193641674237296732

bot = interactions.Client(token=BOT_TOKEN)

base_command = SlashCommand(
    name= "pls",
    description= "work"
)
@base_command.subcommand(sub_cmd_name="Begging you to work", sub_cmd_description=" istg u better not gimme an error")
@slash_option(name= "i think we work", required= False, description=" i better work", opt_type=OptionType.STRING)

if __name__ == '__main__':
    # Code to execute when the script is run as the main program
    try:
        bot.start()
    except Exception as e:
        print(f"An error occurred: {e}")