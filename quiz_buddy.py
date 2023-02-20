import requests
import json, random, string, time, sys
from termcolor import colored, cprint


def main():
    cprint('Welcome to quiz buddy :) !! ', 'blue')
    print('')
    while True:
        print('These are the following quiz category available on quiz buddy :  ')
        url = get_categories()
        get_quiz(url)
        print()
        play = input('Would you like to play again (Yes(y) / No(n or any key) : ').lower()
        if play not in ['y', 'yes']:
            cprint('Byeeeeee!!', 'blue')
            break
        print()

def get_categories():
    
    url = 'https://opentdb.com/api_category.php'
    resp = requests.get(url)
    cat = resp.json()
    categories = { num : cat for num, cat in enumerate(cat['trivia_categories'], start=1)}
    
    for i in categories.keys():
        print(f"{i}. {categories[i]['name']}")
    print(' ')
    cat_input = input('Enter the category number you want : ')
    
    while isinstance(cat_input, int) == False:
        try:
            cat_input = int(cat_input)
            while cat_input not in list(categories.keys()):
                cprint(f'Error: "{cat_input}" is an invalid category number!!', 'red')
                print()
                cat_input = input('Enter the category number you want : ')
                cat_input = int(cat_input)
                
        except:
            cprint(f'Error: "{cat_input}" is not a valid number', 'red')
            print()
            cat_input = input('Enter the category number you want : ')
        
    category = categories[cat_input]['id']
    
    print()
    
    mode = input('Pick difficulty level ( easy, medium, hard ) : ').lower()
    
    while mode not in ['easy', 'medium', 'hard']:
        cprint(f'Error: {mode} is invalid!', 'red')
        print()
        mode = input('Pick difficulty level ( easy, medium, hard ) : ').lower()
        
    print()
    no_q = input('Enter the numbers of questions you would like to do : ')
    
    while isinstance(no_q, int) == False:
        try:
            no_q = int(no_q)
            while no_q > 20:
                cprint('Total number of questions should not be more than 20', 'red')
                print()
                no_q = input('Enter the numbers of questions you would like to do: ')
                no_q = int(no_q)           
        except:
            cprint(f'Error: {no_q} is not a valid number!!', 'red')
            print()
            no_q = input('Enter the numbers of questions you would like to do: ')
            
    print()
    f_url = f'https://opentdb.com/api.php?amount={no_q}&category={category}&difficulty={mode}&type=multiple'
    return f_url
    
def get_quiz(url):
    x = requests.get(url)
    
    quiz = x.json()
    results =quiz['results']
    
    questions = [result['question'] for result in results]
    
    opt = [ (result['incorrect_answers'] + [result['correct_answer']]) for result in results]
    
    answers = [result['correct_answer'] for result in results]
    
    score = 0
    ans_options = {}

    for num, quest in enumerate(questions, start=1):
        print(f'{num}) {quest}')
        print('---------------------------')
        
        index = num
        index -= 1
        
        options = opt[index]
        
        random.shuffle(options)
        
        ans_dict = {i : word for i, word in zip(string.ascii_uppercase, options)}
        
        
        for i, word in ans_dict.items():
            print(f"{i}) {word}")
            
            if answers[index] == word:
                ans_options.update({index + 1: {i : word}})
        
        print('')
        print('(        Enter your answer        )')
        ans = input('My answer : ').upper()
        
        while ans not in list(ans_dict.keys()):
            cprint(f'Your input: "{ans}" is not among the options :( ', 'red')
            ans = input('My answer : ').upper()
        
        if ans_dict[ans] == answers[index]:
            score += 1
            
        print('')
        if index < (len(questions) -2):
            print('..... Next question .....')
        elif index == (len(questions) - 2):
            print('..... Final question .....')
        else:
            cprint('............ Result :) ............', 'blue')
        print('')
        time.sleep(2)
        
     #score
    score = int(score / len(questions) * 100)
    cprint(f'Well done! You scored: {score}%. Congratulations!!! :)  ' if score > 75 else f"You scored: {score}% :(. Don't worry about it, these results aren't even that important anyway", 'blue')
    print()
    
    cprint('............ Solutions ..............', 'green')
    
    print()
    for num, value in ans_options.items():
        for key, val in value.items():
            cprint(f' {num} ==> {key} ({val})', 'green')

if __name__ == '__main__':
    main()