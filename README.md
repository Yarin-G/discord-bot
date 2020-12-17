# discord-moderator-bot
<p align="center">
  <img alt="bot.py" src="https://github.com/Yarin-G/images/blob/master/discord_bot_images/logo.jpg" width="750px">
</p>



* Make your server moderation easier with this moderator bot
* add this bot to couple of different servers in the same time
* Ban, kick and warn users with one command
* easy to use commands
* this bot will save all users warnings in your server using warnings.json file
* add custom commands for every different server
* default bot's prefix is '/'

#### Requirements
* get `pip`
* Download requirements using `pip install -r requirements.txt`
* Clone this repository and run `python bot.py`

### Add Bot
* go to applications in [discord_developer_portal](https://discord.com/developers/applications)
* create a new application
* create a bot and enable the two 'Privileged Gateway Intents' intents
* click on 'copy' under bot token and paste it in 'bot.py' variable named 'TOKEN'
* go to 'OAuth2'
* click on 'bot' check box under 'SCOPES'
* click on 'Administrator' check box under 'BOT PERMISSIONS'
* copy the link displayed in 'SCOPES' section and paste it in your browser
* select the server which the bot will be added to

### Commands
***type `/help` in the server to see this list***<br />
* `/ping` - get the bot response time
* `/server-info` - get an information about the server
* `/role-info [@role]` - get the numeric permissions which speccific role can use
* `/info [@user]` - get user's information (admin permission required)
* `/mute [@user/all]` - mute specific user or type 'all' to mute everyone in a voice channel you are connected to. Note, by default when running `/mute`, bot will mute everyone in a voice channel you are connected to (admin permission required)
* `/unmute [user]` - unmute specific user or type 'all' to unmute everyone in a voice channel you are connected to. Note, by default when running `/unmute`, bot will unmute everyone in a voice channel you are connected to (admin permission required)
* `/timer [time]` - set a timer
    time should be in this format (X = number):<br />
        timer Xh - sets a timer for X hours<br />
        timer Xm - sets a timer for X minutes<br />
        timer Xs / X - Xh - sets a timer for X seconds
* `/timer [time]` - generate an invite link to the server
* `/echo [msg]` - bot will return after what you typed (admin permission required) 
* `/kick [@user] [reason]` - bot will kick the user out of the server (admin permission required) 
* `/ban [@user] [reason]` - bot will ban the user from the server (admin permission required) 
* `/warn [@user] [reason]` - bot will warn a user (admin permission required)
* `/warns [@user] [reason]` - bot will send all user's warns
* `/clear-warns [@user] [reason]` - bot will clear users's warnings (admin permission required)
* `/clear [amount]` - bot will delete messages from text channel (admin permission required)
* `/add-command [command_name] [reply]` - add custom command to the server, the bot will reply with the parameter [reply] (admin permission required)
* `/del-command [command_name]`- delete custom command in current server (admin permission required)
* `/custom-commands` - show all custom commands in current server
