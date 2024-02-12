from config_data.config import load_config

config = load_config('/home/alexander-popkov/Python/TG_bot_template_loaded/bot_template/.env')

bot_token = config.tg_bot.token
superadmin = config.tg_bot.admin_ids[0]
