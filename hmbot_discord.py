import discord
import asyncio
from discord.ext import commands
import hangman_bot
import hmbot_token


bot = commands.Bot(command_prefix = '.')


@bot.event
async def on_ready():
    '''
    Prints to console when bot is initialized
    '''
    print('Bot is ready.')
    activity = discord.Game(name=".commands")
    await bot.change_presence(status=discord.Status.idle, activity=activity)




@bot.command(name='hangman')
async def hangman(ctx):
    '''
    Command plays a game of hangman against the computer
    * Player is given 3 warnings which get subtracted if
      the player guesses anything that is not in the available_letters
      list
    * Player is given 6 guesses only subtracted when their guess is not
      in the secret_word. 
    '''
    game = hangman_bot.HangMan()
    warnings = 3
    guesses = 6
    
    await ctx.send(f'''


**{ctx.author.name}**: 
Your secret word is **{len(game.secret_word)}** letters long!
{game.secret_word}
    ''')
    while True:
        game.get_guessed_word()
        await ctx.send(f'''
You have **{guesses}** guesses left!
Your available letters are: **{game.get_available_letters()}**
Enter **\'*\'** to see all possible matches in the words list
Your guessed word is 
`{game.word_guessed}`
        ''')
        letter = await bot.wait_for('message',
        check=lambda message: message.author == ctx.author, timeout = 500)
        if letter.content.lower() == '*':
            game.show_possible_matches()
            print(len(game.wl))
            if len(game.wl) < 75:
                await ctx.send(f'''
Possible words are:
**{game.wl}**
                ''')
            else:
                await ctx.send('''
**Sorry, The list of possible words isn\'t small enough. 
Please guess more and try again.**
                               ''')
                continue

        elif letter.content.lower() in game.get_available_letters():
            game.letters_guessed.append(letter.content.lower())
            if letter.content.lower() not in game.secret_word:
                guesses -= 1
        else:
            warnings -= 1
            await ctx.send(f'''
Please choose a letter from the list
You have **{warnings}** warnings left
            ''')
            if warnings == 0:
                ctx.send(f'''
You\'ve ran out of warnings
Your secret word was **{game.secret_word}**
                ''')
                break
            else:
                continue
        await ctx.send(f'''{game.physical_hangman(guesses)}''')
        if guesses == 0:
            await ctx.send(f'''
Sorry you ran out of guesses. 
Your secret word was **{game.secret_word}**
            ''')
            break
        if game.is_word_guessed() == True:
            await ctx.send(f'''
Congratulations! You win! Your word was **{game.secret_word}**
You had **{guesses}** guesses remaining
            ''')
            break

bot.run(hmbot_token.token)
