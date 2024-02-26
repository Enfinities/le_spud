import interactions
from interactions import SlashCommand
from decouple import config

BOT_TOKEN = config('BOT_TOKEN1')
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1193641674237296732

bot = interactions.Client(token=BOT_TOKEN)

base_command = SlashCommand(
    name="pls",
    description="work"
)

@base_command.subcommand(sub_cmd_name="Begging you to work", sub_cmd_description="istg u better not gimme an error")
@slash_option(name="i think we work", required=False, description="i better work", opt_type=OptionType.STRING)
async def command_name(ctx: interactions.CommandContext, option: bool = None):
    """A descriptive description"""
    await ctx.send(f"You selected the command_name sub command and put in {option}")

# Check the indentation of the following block
if __name__ == '__main__':
    try:
        bot.start()
    except Exception as e:
        print(f"An error occurred: {e}")