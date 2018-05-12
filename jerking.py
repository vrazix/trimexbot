import re
import random
import datetime
from dateutil import parser
from dateutil import relativedelta
import pprint

__version__ = '0.69'

class Jerk(object):
    def __init__(self, date, number, title, text):
        '''Date uses datetime.date objects'''
        self.date = date
        self.num = number
        self.title = title
        self.raw_text = text

        self.process_text()

    def process_text(self):
        self.characters = set()
        self.lines = []
        for line in self.raw_text:
            try:
                character, line = line.split(':', 1)
            except ValueError:
                self.lines.append(line)
                continue
            self.characters.add(character)
            self.lines.append(line)

    def __repr__(self):
        return 'num={num}, date={date}, title={title}, raw_text={raw_text}'.format(**self.__dict__)

def load_jerks(fn='jerkcity_full.txt'):
    '''Load the jerkcity.com/jerkcity.txt format into a list of Jerk objects'''

    with open(fn, 'r') as inf:
        next(inf) # first line just says how many acts are in the play
        jerk_objs = []
        cur_text = []
        cur_date, cur_name, cur_title = '1/1/1980', 'NaN', '!ERROR!'
        for line in inf:
            if re.search('JERKCITY #\d+:', line):
                try:
                    cur_num, cur_title = re.search('JERKCITY #(\d+):\s+(.*)\n', line).groups()
                    cur_num = int(cur_num)
                except AttributeError:
                    print(line)
            elif re.search('\d+/\d+/\d+', line):
                date_string = re.search('(\d+/\d+/\d+)', line).group(1)
                month, day, year = map(int, date_string.split('/'))
                cur_date = datetime.datetime(year, month, day)
            #elif re.search(':\S+', line):
            #    cur_text.append(line)
            elif re.match('--cut here--', line):
                jerk_objs.append(Jerk(cur_date, cur_num, cur_title, cur_text))
                cur_text = []
            elif re.search('\S+', line):
                cur_text.append(line[:-1])

    return jerk_objs

def find_jerk(jerk_objs, phrase):
    '''Return a list of jerk objects that contain lines matching the phrase.

    Also returns the list of lines that trigger the match.'''

    tagged_jerks = []
    tagged_lines = []
    for jerk in jerk_objs:
        for line in jerk.lines:
            if re.search(phrase.upper(), line):
                tagged_jerks.append(jerk)
                tagged_lines.append(line)
                break

    return tagged_jerks, tagged_lines

def find_hulag(jerk_objs):
    '''Find a fuckin' hulag who cares'''

    hulags = {}
    for jerk in jerk_objs:
        for line in jerk.lines:
            if re.search('(H[HBULAG]+)\s', line):
                hulag = re.search('(H[HBULAG]+)\s', line).group(1)
                if set(hulag) == {'H', 'A'} or set(hulag) == {'H', 'U'}:
                    continue
                if hulag in hulags.keys():
                    hulags[hulag] += 1
                else:
                    hulags[hulag] = 1

    return hulags

def just_lines(jerk_objs):
    '''Return a list of lines from the jerk_objs'''

    all_lines = []
    for jerk in jerk_objs:
        all_lines += jerk.lines
    return all_lines

def find_by_date(jerk_objs, date_string):
    '''Return the Jerk with the minimum distance to date_string (parsed by dateutil)'''

    try:
        date = parser.parse(date_string)
    except ValueError:
        return 'Unable to parse date!'
    return sorted(jerk_objs, key=lambda x: abs(date - x.date))[0]

def find_by_num(jerk_objs, num):
    '''Return the jerk_obj that has num'''
    try:
        return list(filter(lambda x: x.num == int(num), jerk_objs))[0]
    except IndexError:
        random.choice(jerk_objs)

if __name__ == '__main__':
    jerk_objs = load_jerks()

    bychar = lambda jerk: len(jerk.characters)

    jerkchar = sorted(jerk_objs, key=bychar)

    print(jerkchar[0])
    print(jerkchar[-1])

    raise SystemExit
    
    hulags = find_hulag(jerk_objs)
    #pprint.pprint(hulags)
    #print(len(hulags))

    #print(find_jerk(jerk_objs, 'mumbo'))

    #print(random.choice(list(find_hulag(jerk_objs).keys())))

    phrase = 'mumbo'
    jerks, lines = find_jerk(jerk_objs, phrase)
    jerk, line = random.choice(list(zip(jerks, lines)))
    #print('{} (Comic #{})'.format(line, jerk.num))

    #print(find_by_date(jerk_objs, 'may 8 2001').date)
    #print(find_by_date(jerk_objs, 'may 8 2002'))

    print(find_by_num(jerk_objs, '4163'))

    j, l = find_jerk(jerk_objs, 'folks')
    print(len(j), len(l))