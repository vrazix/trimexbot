import discord # version 0.16.7
from discord.ext import commands
import random, re
import jerking, cubing # versions 0.69 (both.)
import nltk # version 3.2.5

description = 'A bot for boys'

# list of 'thinking' emojis from trimethylxanthine
THOUGHTS = [':assthonk:376075749217665025', ':thinkplant:376083296389562369', ':thinksweat:376075735502422026', ':thinkling:338029126176997380', ':thinkwater:365216695842897920', ':thoughting:326044010382884865', ':thoughts:396531476054802434']  

# global variable to hold the last two messages in chat. don't @ me
# also this doesn't persist between channels so it's technically wrong!!!
LAST_TWO_MESSAGES = []

def prefixer(self, message):
    '''command_prefix callable to handle messages from the irc bot.

    Parses **<user>** !::command::'''

    try:
        print('{}: {}'.format(message.author.name, message.content))
    except UnicodeEncodeError:
        print('UnicodeBoye: {}'.format(message.content))
    if message.author.name.lower() == "irc":
        m = re.match(r'^\*\*<[^>]*>\*\* !', message.content)
        if m:
            return m.group()
    return '!'

bot = commands.Bot(command_prefix=prefixer, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def buttify(message):
    # TODO figure out a way to preparse out things like URLs, emojis and tags
    tagged = nltk.pos_tag(nltk.word_tokenize(message.content))
    print(tagged)
    enumerated = [(i, word, token) for i, (word, token) in enumerate(tagged)]
    nouns = list(filter(lambda x: x[2] in ['NN', 'NNS', 'NNP'], enumerated))

    def how2butt(word, token):
        try:
            if token == 'NN':
                if word[0].islower():
                    butt = 'butt'
                elif word.isupper():
                    butt = 'BUTT'
                else:
                    butt = 'butt'
            elif token == 'NNS':
                if word[0].islower():
                    butt = 'butts'
                elif word.isupper():
                    butt = 'BUTTS'
                else:
                    butt = 'butt'
            elif token == 'NNP':
                if word.isupper():
                    butt = 'BUTTS'
                else:
                    butt = 'Butts'
        except:
            butt = 'butt'

        return butt

    guaranteed_index = random.choice(nouns)[0]

    butted = ''

    for i, word, token in enumerated:
        chance = random.random()

        if i == guaranteed_index:
            butted += ' ' + how2butt(word, token)
        elif token in ['NN', 'NNS', 'NNP']:
            if chance > 0.75:
                butted += ' ' + how2butt(word, token)
            else:
                butted += ' ' + word

        # check if the word is alpha to guess that we need to space it
        elif word.isalnum():
            butted += ' ' + word

        elif 'http' in word or 'www' in word:
            continue

        else:
            butted += word

    return butted


@bot.listen()
async def on_message(message):
    # keep track of the last two messages for !hmm
    global LAST_TWO_MESSAGES
    if len(LAST_TWO_MESSAGES) < 2:
        LAST_TWO_MESSAGES.append(message)
    elif len(LAST_TWO_MESSAGES) == 2:
        LAST_TWO_MESSAGES = [LAST_TWO_MESSAGES[1], message]

    # decide if we're gonna butt it up
    chance = random.random()
    if chance > 0.975:
        content = buttify(message)
        if content:
            await bot.send_message(message.channel, content=content)
    
    # i used to think i needed this because the docs said so
    # then i learned that was a lie. this is a monument to being
    # lied to by the docs. f u.
    #await bot.process_commands(message)


@bot.command()
async def gayjerk(*phrase: str):
    jerks, lines = jerking.find_jerk(jerk_objs, ' '.join(phrase))
    if not jerks:
        await bot.say(random.choice(random.choice(jerk_objs).lines))
    else:
        jerk, line = random.choice(list(zip(jerks, lines)))
        await bot.say('{} (Comic #{} [{}])'.format(line, jerk.num, len(jerks)))


@bot.command()
async def bonequest(*phrase: str):
    jerks, lines = jerking.find_jerk(jerk_objs, ' '.join(phrase))
    if not jerks:
        await bot.say(random.choice(random.choice(jerk_objs).lines))
    else:
        jerk, line = random.choice(list(zip(jerks, lines)))
        await bot.say('{} (Comic #{} [{}])'.format(line, jerk.num, len(jerks)))


@bot.command()
async def hulag():
    await bot.say(random.choice(list(jerking.find_hulag(jerk_objs).keys())))


@bot.command()
async def jerkdate(*date: str):
    jerk = jerking.find_by_date(jerk_objs, ' '.join(date))
    await bot.say('{} (Comic #{}) {}'.format(''.join(jerk.lines), jerk.num, jerk.date))


@bot.command()
async def comic(num: int):
    if num < 0:
        jerk = random.choice(jerk_objs)
    else:
        jerk = jerking.find_by_num(jerk_objs, num)
    multiline = 'Comic #{}: {}, {}\n'.format(jerk.num, jerk.title, jerk.date)
    multiline += '\n'.join(jerk.raw_text)
    await bot.say('```{}```'.format(multiline))


@bot.command()
async def comice(num: int):
    lines = jerking.find_by_num(jerk_objs, num).raw_text
    new_lines = []
    for line in lines:
        if re.match('spigot:', line):
            new_line = re.sub('^spigot', '<:spigot:370560055361273867>', line)
        elif re.match('pants:', line):
            new_line = re.sub('^pants', '<:pants:370560091801255947>', line)
        elif re.match('deuce:', line):
            new_line = re.sub('^deuce', '<:deuce1:370563819925405696>', line)
        elif re.match('rands:', line):
            new_line = re.sub('^rands', '<:rands:370562621457301507>', line)
        elif re.match('bung:', line):
            new_line = re.sub('^bung', '<:bung:370562689199505408>', line)
        else:
            new_line = line
        new_lines.append(new_line)
    await bot.say('{}'.format('\n'.join(new_lines)))


@bot.command()
async def thoughts():
    thoughts = THOUGHTS
    random.shuffle(thoughts)
    await bot.say(' '.join(['<{}>'.format(_) for _ in thoughts]))


@bot.command()
async def timecube(*phrase: str):
    found_cubes = cubing.find_cube(cubes, ' '.join(phrase))
    if not found_cubes:
        await bot.say(random.choice(cubes))
    else:
        await bot.say('{} [{}]'.format(random.choice(found_cubes), len(found_cubes)))
    

@bot.command()
async def hmm():
    global LAST_TWO_MESSAGES
    message = LAST_TWO_MESSAGES[1]
    thoughts = THOUGHTS
    random.shuffle(thoughts)
    for thought in thoughts:
        await bot.add_reaction(message, thought)

jerk_objs = jerking.load_jerks()
cubes = cubing.load_cubes()

#bot.run('secret')