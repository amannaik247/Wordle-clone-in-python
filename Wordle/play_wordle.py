from wordle import Wordle
from colorama import Fore
from typing import List
from letter_state import LetterState
import random

def main():

    word_set = load_word_set("Wordle\\data\\wordle_words.txt")
    secret = random.choice(list(word_set))
    print("Hello User")
    wordle = Wordle(secret)

    while wordle.can_attempt:
        x = input("\nEnter guess: ")
        x = x.upper()
        if len(x) != wordle.WORD_LENGTH:
            print(Fore.RED 
                  + f"Word must be {wordle.WORD_LENGTH} characters long"
                  + Fore.RESET) 
            continue

        if not x in word_set:
            print(
                Fore.RED
                + f"{x} is not a valid word"
                + Fore.RESET
            )
            continue

        wordle.attempt(x)
        display_results(wordle)
       
    if wordle.is_solved:
        print("You won the game")
    else:
        print(Fore.RED + "You lost" + Fore.RESET)
        print(f"The secret word was: {wordle.secret}")
def display_results(wordle: Wordle):
    print(f"\nYou have {wordle.remaining_attempts} remaining guesses\n")

    lines = []

    for word in wordle.attempts:
        result = wordle.guess(word)
        colored_result_str = convert_result_to_color(result)
        lines.append(colored_result_str)

    for _ in range(wordle.remaining_attempts): # underscore is used as placeholder as we wont use that variable again 
        lines.append(" ".join(["_"] * wordle.WORD_LENGTH))
 
    draw_border_around(lines)

def load_word_set(path: str):
    word_set = set()
    with open(path, "r") as f:
        for line in f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set

    
def convert_result_to_color(result: List[LetterState]):
    result_with_color = []
    for letter in result:
        if letter.is_in_position: 
            color = Fore.GREEN
        elif letter.is_in_word:
            color = Fore.YELLOW
        else:
            color = Fore.WHITE

        colored_letter = color + letter.character + Fore.RESET
        result_with_color.append(colored_letter)
    return " ".join(result_with_color)
    
def draw_border_around(lines: List[str], size: int = 9, pad = 1):
    content_length = size + pad * 2
    top_border = "┌" + "─" * content_length + "┐"
    bottom_border = "└" + "─" * content_length + "┘"
    space = " " * pad # For space between left and right edges
    print(top_border)

    for line in lines:
        print("│" + space + line + space + "│")
        
    print(bottom_border)

if __name__ == "__main__":
    main()