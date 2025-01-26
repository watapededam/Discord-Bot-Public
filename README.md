# Discord Bot Template
This repository contains a Discord bot built with discord.py version 2.x. The bot uses Python 3.11 and is designed to load extensions dynamically and handle basic logging and configuration. Below is a step-by-step guide to set up, run, and manage the bot.

# Prerequisites:
Before running the bot, ensure the following components are installed: 
## 1. Python 3.11: 
Download and install Python 3.11 from the official Python website (https://www.python.org/downloads/). 
## 2. pip: Ensure pip (Python's package installer) is installed.
It is usually included with Python. You can check by running 
```pip --version```
## 3. Discord API Token: 
Create a bot on the Discord Developer Portal (https://discord.com/developers/applications) and retrieve your bot's token. 
## 4. Supervisor (for keeping the bot running permanently): 
Install Supervisor using your system's package manager with 
```sudo apt update && sudo apt install supervisor```

# Installation 
## Steps: 1. Clone the repository: 
Clone the bot repository to your local machine with 
```git clone https://github.com/watapededam/Discord-Bot-Public.git && cd Discord-Bot-Public``` 
## 2. Set up a virtual environment (optional but recommended): 
Create and activate a virtual environment with ```python3.11 -m venv venv && source venv/bin/activate```
## 3. Install dependencies: 
Install the required Python packages listed in requirements.txt using ```pip install -r requirements.txt```
## 4. Set up environment variables: 
Create a ```.env``` file in the root directory and add your Discord bot token as ```TOKEN=your_discord_bot_token```
## 5. Configure the bot: 
Create a config.json file in the root directory with the required configuration. Example: ```{"bot_channel": 123456789012345678}```

# Running the Bot: 
To start the bot, simply run ```python main.py```

# Running the Bot Permanently with Supervisor: 
## 1. Create a Supervisor configuration file: 
Create a configuration file for the bot in ```/etc/supervisor/conf.d/discord_bot.conf``` with the following content: 
```
[program:discord_bot] 
command=/path/to/venv/bin/python /path/to/Discord-Bot-Public/main.py
directory=/path/to/Discord-Bot-Public
autostart=true
autorestart=true
stderr_logfile=/var/log/discord_bot.err.log
stdout_logfile=/var/log/discord_bot.out.log
user=your-username
```
## 2. Update Supervisor and start the bot: 
Reload Supervisor to apply the changes with ```sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl start discord_bot```
## 3. Monitor the bot logs: 
Check the logs to ensure the bot is running using ```sudo tail -f /var/log/discord_bot.out.log```

# Additional Notes: 
To reload the bot's configuration or extensions, use the appropriate Discord commands (!reload or !extension). For debugging or maintenance, stop the bot with sudo supervisorctl stop discord_bot. Ensure the cogs folder is properly populated with your bot's extensions.
# Developing Additional Features:
To develop additional features or extend the bot's functionality, refer to the official `discord.py` documentation available here: [https://discordpy.readthedocs.io/en/stable/](https://discordpy.readthedocs.io/en/stable/)

# License:
This project is licensed under the MIT License.
