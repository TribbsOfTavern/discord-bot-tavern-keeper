# discord-bot-tavern-keeper
A discord bot created for my friends and I to enjoy in discord. It is largely Dungeons and Dragons themed.

## __Some quick info__
This discord bot is run locally at the moment as well as mongodb. Creating a clone of it isn't impossible, but currently running it as is will not be able to call many of the information commands as is. So I added some schema functions to the dndMongo.py file to help with understanding my collections as well as for adding homebrew in at a later date.

Also this is my first publically shared project. Figured it would help me with my confidence level a bit when it came to writing code.

  ## __Commands with this bot__
  - !ping &ensp;&ensp; because its kind of a basic in learning how to send and reply to messages
  
  - !roll <dn> &ensp;&ensp;will take dice notation and return the results (2d6, 2d20kh1, 2d20kl1)
  
  - !roll_character &ensp;&ensp;will provide you with a basic random 5e D&D character unless you provide options
    - level=<1-20>  &ensp;&ensp;  sets level. Invalid returns level 1
    - class=<class>  &ensp;&ensp;  sets class. invalid returns random class
    - race=<race>   &ensp;&ensp;  sets race. invalid returns a random race
    - background=<background>  &ensp;&ensp;  sets background. invalid returns random background
    - rolls=<dn>  &ensp;&ensp;  sets the style for rolling your stats. invalid returns 3d6 stats
  
  - !spell <spell name>&ensp;&ensp;will return information regarding a spell. **This only currently works with my mongodb collection
  
  - !item <item name> &ensp;&ensp;will return information regartding an item. **This only currently works with my mongodb collection
  
  - !monster <monster name>&ensp;&ensp;will return information regarding a monster. **This only currently works with my mongodb collection
  
  - !draw | !draw <#> &ensp;&ensp; will draw a number of cards from the server deck and return them. limited from 1 to 52
  
  - !fightme  |  !fightme --force  &ensp;&ensp;  will give you a 50-50 shot at defeating the tavern keeper. If you lose and are in a voice channel they will kick you from voice. If you are the server owner you have to --force the fight.
  
  - !coinflip | !coinflip <heads|tails> &ensp;&ensp; will flip and coin and return the result. If you called the flip it will also announce if you've won or lost.

## __Server Owner Only Commands__
- !settings <setting> <opt>
  - channel <text-channel> &ensp;&ensp;  will restrict the bot to only respond to commands in the server to a specified channel
  - silent <true|false> &ensp;&ensp;  will set the notification blip to either be off(silent true) or on(silent false)

- !clean <#> <text-channel> &ensp;&ensp; will purge the commanded channel (or specified channel) or the number of messages expressed. Newest to Last. By default !clean will remove 100 messages from the channel the command is given.

- !peakdeck &ensp;&ensp; Allows the owner to peak at the server deck, which is always stocked.

- !test <*args*> &ensp;&ensp; does nothing really and I really only used it for learning how discordpy handled *args, if your wondering, *arg gives you a tuple of strings. ie '!somecommand a 2 c 4' would get you  args=('a', '2', 'c', '4')

  
  ## __Commands not yet implemented__
  - !createdeck <type> <name>  &ensp;&ensp;  will create and save a deck of the type you specified.
  - !drawdeck <name> <#>  &ensp;&ensp;  will allow you to pull a card from a named deck.
