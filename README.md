# GMTK Game Jam Bot

A simple Discord bot to power the slash commands and auto-responder we use in the game jam.

(Please ignore references to redbot, it's not a thing any more)

## How does it work

There's a DigitalOcean droplet (`134.122.111.73`) that runs the Python code to power the bot.

Whenever the `main` branch changes, the [GitHub Action](.github/workflows/deploy.yml) will trigger the server to run `git pull` (to update the local code) and `systemctl restart` (to run the updated code).

The SSH config etc. is all set up as [secrets here](https://github.com/Willdotwhite/gmtk-red-bot-cog/settings/secrets/actions). It shouldn't need changing unless the droplot goes away.
