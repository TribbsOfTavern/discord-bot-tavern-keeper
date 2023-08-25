# discord-bot-tavern-keeper
A discord bot created for my friends and I to enjoy in discord. It is largely Dungeons and Dragons themed.

### __Some Quick Info__
This discord bot is run locally at the moment as well as mongodb. Creating a clone of it isn't impossible, but currently running it as is will not be able to call many of the information commands as is. So I added some schema functions to the dndMongo.py file to help with understanding my collections as well as for adding homebrew in at a later date.

Also this is my first publically shared project. Figured it would help me with my confidence level a bit when it came to writing code.

### __User Commands__
| Command     | Opts | Description                               |
| ----------- | ---- | ----------------------------------------- |
| **!ping**   | |your basic call-response                       |
| **!roll** | | return a result of the roll notation |
| * *required* | *roll-notation* |  ie 2d6 or 2d20kh1 or 2d20kl1  | 
| **!roll_character** | | returns a randomly generated level 1 D&D 5e character. |
| * *optional* | level=*1-20* | set the level of the character rolled, invalid input will return level 1 |
| * *optional* | class=*class-name* | set the class for the character rolled, invalid input will return a random class |
| * *optional* | race=*race-name* | set the race for the character rolled, invalid input will return a random race |
| * *optional* | background=*background* | set the background for the character rolled, invalid input will return random background |
| * *optional* | rolles=*roll-notation* | set the roll notation for stat rolls, default is 3d6 but 4d6kh3 is a more common way to roll |
| **!draw** | *1-52* | draw a number of cards from the server deck |
| **!fightme** | | fight the Tavern Keeper with a 50-50 chance to win, if you are in voice and lose it kicks you from voice. |
| * *optional* | *--force* |  Server owners need to use *--force* |
| **!coinflip** | | flip a coin and get results |
| * *optional* |  *heads* or *tails* | if a call was made will also announce if you won or lost |
| **!createdeck** | | create a deck with a name of a certian type |
| * *required* | *type* | 'standard', 'domt', 'tarot-full', 'tarot-major', 'tarot-minor' |
| * *required* | *name* | name of the deck that must not contain spaces |
| * *optional* | *auto_shuffle* | True or False. If True when the last card is pulled the deck will reshuffle. |
| **!drawdeck** | | draw from a specified deck |
| * *required* | *deck-name* | |
| **!reshuffle** | | reshuffle a specified deck, must be deck author |
| * *required* | *deck-name* | |
| **!removedeck | | remove a specified deck from the list of decks on the server, must be the author or server owner |
| * *required* | *deck-name* | |
| **!revealdeck | | reveal a specified decks pile and discard pile, must be the deck author |
| * *required* | *deck-name* | |

### __Server Owner Commands__
| Command     | Opts | Description                               |
| ----------- | ---- | ----------------------------------------- |
| **!settings channel** | | set the text-channel for the bot to reply to commands in |
| * *required* | *channel-name* | |
| **!settings silent** | | set if the bot's reply messages should be muted or not
| * *required* | *True* or *False* | |
| **!clean** | | purge the last 100 messages of the channel the command was input |
| * *optional* | *number* | change the number of messages to purge |
| * *optional* | *text-channel* | specify the channel the bot will purge messages from |
| **!peakdeck** | | get the current stock in the server playing card deck |

