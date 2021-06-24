import logging as log

log.basicConfig(level=log.INFO, format='%(levelname)s: %(message)s')

if __name__ == 'lib.helper':
    log.info('helper.py loaded')

def log_guilds(bot):
    guildstr = ""
    for guild in bot.guilds:
        guildstr += str(guild) + ' ('+ str(guild.id) +')' + "\n"
        pass
    log.info('We are logged in as '+bot.user.name+' in:\n'+guildstr)
