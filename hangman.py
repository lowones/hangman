#!/usr/bin/python
import time
import argparse
import requests
import random
import os
import json
import random
ERASE_LINE = '\x1b[2K'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

a = 97
z = 123
delay = .01
CURSOR_UP_ONE = '\x1b[1A'
BACKUP = 'global to hold lines to backup for flourish to work, changed after clear'

def main():
    print("lets play hangman")
    defined = False
    reveal = False
    hint = False
    topic = ''
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', nargs='+', type=str, required=False, help='Topic of word')
    parser.add_argument('-H', action='store_true', required=False, help='Provide hint on last guess')
    parser.add_argument('-d', action='store_true', required=False, help='Word must have definition')
    parser.add_argument('-D', action='store_true', required=False, help='Reveal definition with guesses, not scored')
    args = parser.parse_args()
    if args.t:
        topic = ' '.join(args.t)
    if args.H:
        hint = True
    if args.d:
        defined = True
    if args.D:
        reveal = True
        defined = True
    hangman(topic, defined, hint, reveal)

def hangman(topic, defined, hint, reveal):
    global BACKUP
    no_def = "no definition found for "
    while True:
        word = get_word(topic)
        definition = define(word)
        if not definition:
            definition = define(word[:-1])
            if not definition:
                definition = no_def + word
        if defined and definition.startswith(no_def):
            continue
        else:
            break
    solution = build_solution(word)
    def_sol = build_solution(definition)
    print(solution)
    available_letters = get_alphabet()
    attempts_left = 5
    status = ''
    while True:
        os.system('clear')
        BACKUP=14
        print("\n\n%s\n\n%s\n\n%s\n\n" % (solution, status, available_letters))
        draw_score(attempts_left)
        if reveal and not attempts_left == 0:
            print("\n%s\n" % def_sol)
            BACKUP+=(3+definition.count('\n'))
        if attempts_left == 0 and hint:
            if definition.endswith(word):
                print("\n%s\n" % 'no definition found')
                BACKUP+=1
            else:
                print("\n%s\n" % definition)
                BACKUP+=(3+definition.count('\n'))
        guess = guess_letter = get_guess_letter(available_letters)
        f(available_letters)
        available_letters = update_available_letters(guess, available_letters)
        fs(guess, solution, word)
        (found, solution) = update_solution(guess, solution, word)
        if reveal:
            if definition.endswith(word):
                print("\n%s\n" % 'no definition found')
                BACKUP+=1
            else:
                (ignore, def_sol) = update_solution(guess, def_sol, definition)
        if solution == word:
            os.system('clear')
            print("\n\n%s\n\nYou WON!!!\t%s\n\n" % (word, attempts_left))
            draw_score(7)
            break
        else:
            if found:
                status = "Good guess..."
            else:
                if attempts_left:
                    status = ("There is no %s in the word" % guess)
                    attempts_left-=1
                else:
                    attempts_left-=1
                    os.system('clear')
                    print("\n\nYou LOST!?!\n\n")
                    print("The answer was: %s\n\n\n\n\n" % word)
                    draw_score(attempts_left)
                    break
    print("\n%s\n" % definition)

def draw_score(score):
    print('\n')
    if score == 5:
        print(" ___")
        print("/   J")
        print("|")
        print("|")
        print("|")
        print("|")
        print("|________")
    elif score == 4:
        print(" ___")
        print("/   J")
        print("|   O")
        print("|")
        print("|")
        print("|")
        print("|________")
    elif score == 3:
        print(" ___")
        print("/   J")
        print("|   O/")
        print("|")
        print("|")
        print("|")
        print("|________")
    elif score == 2:
        print(" ___")
        print("/   J")
        print("|   O/")
        print("|   |")
        print("|")
        print("|")
        print("|________")
    elif score == 1:
        print(" ___")
        print("/   J")
        print("|   O/")
        print("|   |")
        print("|  /")
        print("|")
        print("|________")
    elif score == 0:
        print(" ___")
        print("/   J")
        print("|  \O/")
        print("|   |")
        print("|  /")
        print("|")
        print("|________")
    elif score < 0:
        print(" ___")
        print("/   J")
        print("|  \O/")
        print("|   |")
        print("|  / \\")
        print("|")
        print("|________")
    elif score > 5:
        print(" ___")
        print("/   J")
        print("|")
        print("|")
        print("|          <O")
        print("|           |\\")
        print("|________  / \\")
    print('\n')

def get_word(topic):
    if topic:
        WORDS = get_word_topic(topic)
    else:
        word_file = "/usr/share/dict/words"
        WORDS = open(word_file).read().splitlines()
    word = random.choice(WORDS)
    return word

def get_alphabet():
    alphabet = ''.join(map(chr, range(97, 123)))
    return alphabet

def build_solution(word):
    solution = []
    for index, char in enumerate(word):
        if char.isalpha():
            solution.append('_')
        else:
            solution.append(char)
    solution = ''.join(solution)
    return solution

def get_guess_letter(available):
    global BACKUP
    while True:
        letter = raw_input("Choose a letter from the available letters :  ")
        BACKUP+=1
        if letter in available:
            break
    return letter

def update_available_letters(guess, a_letters):
    c_a_letters = list(a_letters)
    for index, letter in enumerate(c_a_letters):
        if letter == guess:
            c_a_letters[index] = '_'
    new_a_letters = ''.join(c_a_letters)
    return new_a_letters


def update_solution(guess, solution, word):
    found = False
    solution = list(solution)
    for index, letter in enumerate(word):
        if letter.lower() == guess:
            found = True
            solution[index] = letter
    solution = ''.join(solution)
    return (found, solution)


def get_word_topic(topic):
    words = []
    print("topic : %s" % topic)
    r = requests.get('https://api.datamuse.com/words?ml=' + topic)
    words_j = r.json()
    for item in words_j:
        words.append(item['word'])
    return words

def get_topic():
    topic = raw_input("Enter a topic : ")
    return topic


def define(word_id):
    app_id = 'ef70fcb9'
    app_key = 'be5c3d7d0913371ef0c493db364f4d57'
    language = 'en'
    region = 'us'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/regions=' + region

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    definition = False
    if r.status_code == 200:
        word = r.json()
        definitions = get_definitions(word)
        definition = ('\n'.join(definitions))
    return definition

def get_definitions(data):
    if isinstance(data, dict):
        definitions = walk_dict_definitions(data)
    return definitions

def walk_dict_definitions(data):
    d = []
    for key, value in data.items():
        if key == 'definitions':
            d.append(''.join(value))
        elif isinstance(value, dict):
            defs = walk_dict_definitions(value)
            if defs:
                d = d + defs
        elif isinstance(value, list):
            defs = walk_list(value)
            d = d + defs
    return d

def walk_list(data):
    d = []
    for item in data:
        if isinstance(item, dict):
            defs = walk_dict_definitions(item)
            d = d + defs
        elif isinstance(item, list):
            defs = walk_list(item)
            d = d + defs
    return d

def fs(guess, solution, word):
    S_BACKUP=4
    line = 0
    while(line < S_BACKUP):
        line+=1
        sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    flourish_sol(guess, solution, word)

def f(az):
    line = 0
    while(line < BACKUP):
        line+=1
        sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    flourish(az)

def flourish(az):
    alphabet = list(az)
    cycle = 0
    cycles = random.randint(1,3)
    while cycle < cycles:
        cycle+=1
        for index, letter in enumerate(alphabet):
            alphabet[index] = letter.upper()
            print("\r%s" % ''.join(alphabet)),
            sys.stdout.flush()
            time.sleep(delay)
            alphabet[index] = letter.lower()
        for index, letter in reversed(list(enumerate(alphabet))):
            alphabet[index] = letter.upper()
            print("\r%s" % ''.join(alphabet)),
            sys.stdout.flush()
            time.sleep(delay)
            alphabet[index] = letter.lower()

def flourish_sol(guess, solution, word):
    delay = .07
    graphic = list(solution)
    word = list(word)
    for index, letter in  enumerate(graphic):
        word_letter = word[index].lower()
        if word_letter == guess:
            graphic[index] = '*'
        elif  letter == '_':
            graphic[index] = '-'
        print("\r%s" % ''.join(graphic)),
        sys.stdout.flush()
        time.sleep(delay)
        if graphic[index] == '-':
            graphic[index] = '_'
    for index, letter in  reversed(list(enumerate(graphic))):
        if letter == '*':
            graphic[index] = word[index]
        elif  letter == '_':
            graphic[index] = '-'
        print("\r%s" % ''.join(graphic)),
        sys.stdout.flush()
        time.sleep(delay)
        if letter == '-':
            graphic[index] == '_'

def get_alphabet():
    alphabet = ''.join(map(chr, range(a, z)))
    return alphabet

if __name__ == "__main__":
    main()
