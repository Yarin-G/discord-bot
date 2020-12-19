<p align="center">
  <img alt="bot.py" src="https://cdn.discordapp.com/attachments/787269923394682890/789207686608191538/logo.jpg" width="750px">
</p>
<br>

## Features <br>
* ban, kick and warn users with one command<br>
* easy to use commands<br>
* add custom commands to the bot without any coding<br>
* custom welcome messages <br>
* verification system<br>
* automatically add roles to new users<br>

## Setup
#### Requirements
* python 3.6 or higher (https://www.python.org/)
* get `pip`
* Download requirements using `pip install -r requirements.txt`
* Clone this repository and run `python bot.py`

#### Create a Bot App 
1. go to applications in [discord_developer_portal](https://discord.com/developers/applications)
<br>
<p align="center">
  <img src="https://cdn.discordapp.com/attachments/787269923394682890/789207970697183272/steps.png" width="750px">
</p>
<br>
2. create a new application<br>
3. create a bot and enable the two 'Privileged Gateway Intents'<br>
4. open `files/settings.json` and fill the fields (token, prefix, welcomes channel)<br>

#### Add The Bot To Your Server
1. go to 'OAuth2'<br>
2. click on 'bot' check box under 'SCOPES'<br>
3. click on 'Administrator' check box under 'BOT PERMISSIONS'<br>
4. copy the link displayed in 'SCOPES' section and paste it in your browser<br>
5. select your server<br>

***that's it! enjou your bot!***<br>
***launch it and type `.help` to see all the commands!***


## FAQ
Q: I don't see my bot on my server!<br>
A: Invite it by using this URL: https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot<br>
Remember to replace **CLIENT_ID** with your bot client ID


## Welcome Messages
you can write custom different welcome messages to new users<br>
just go to `files/channel_welcome_member_message.txt` or `files/private_welcome_member_message.txt` and type your welcome message.<br>
you can use:<br>
`{user}` - mention the new user<br>
`{members_count}` - display number of memebrs in the server<br>
`{server}` - display the server name


## Custom Commands
you can add custom commands to the bot. just type:<br>
`.add-command <command-name> <bot-reply>`
<br>
the `<command-name>` will be the triger of the command<br>
and `<bot-reply>` will be the bot respond<br>
for example:<br>
`.add-command hello hello how are you?`<br>
 <br>
 if you want to delete a command just type:<br>
 `.del-command <command-name>`
 <br>
 <br>
 to see all custom commands just type:<br>
 `.custom-commands`
  
  
## Verification System
make new users verify themselves<br>
you can edit the verification message in `files/verify_message.txt`<br>
to add the verification message just type `.verify-message` and the bot will send your custom verification message<br>
**note:** make sure to add new role and name it `verified` then place the new role under the bot role


## Automatic Roles
add roles to new users when they join your server<br>
go to `files/settings.json` and in `auto roles` add the roles you want to give to new users,<br>
the bot will automatically add the roles you have typed to new users when they join your server<br>
(you can see an example at `files/settings.json`)<br>
**note:** make sure the bot's role is higher than the roles you want to give.
