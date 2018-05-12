import random, re

def load_cubes(fn='timecube.txt'):
    '''Load a simple timecube.txt (quotes separated by newlines)'''
    cubes = []
    with open(fn, 'r') as inf:
        for line in inf:
            cubes.append(line[:-1])

    return cubes

def find_cube(cubes, phrase):
    tagged = []
    for cube in cubes:
        if re.search(phrase.lower(), cube.lower()):
            tagged.append(cube)
    return tagged

if __name__ == '__main__':
    cubes = load_cubes()
    print(random.choice(cubes))

    print(random.choice(find_cube(cubes, 'rotating')))