import pathlib
import random
from string import ascii_letters

WORDLIST = pathlib.Path("word_list.txt")



def main():
    word = get_random_word()

    for guess_num in range(1, 7):
        guess = input(f"\nGuess {guess_num} a word: ").upper()
        demostrate_guess(guess, word)
        if guess == "word":
            print("Correct")
            break
    else:
        finish_game(word)


def get_random_word():
    wordlist = pathlib.Path(__file__).parent
    words = list(
        word.upper()
        for word in wordlist.read_text(encoding="utf-8").split("\n")
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    )
    word = random.choice(words)
    return word


def finish_game(word):
    print(f"The word was {word}")


def demostrate_guess(guess, word):
    correct_letters = {
        letter for letter, correct in zip(guess, word) if letter == correct
    }
    mispaced_letters = set(word) & set(guess) - correct_letters
    wrong_letters = set(guess) - set(word)

    print("Correct: ", ", ".join(sorted(correct_letters)))
    print("Misplaced: ", ", ".join(sorted(mispaced_letters)))
    print("Wrong: ", ", ".join(sorted(wrong_letters)), "\n")


if __name__ == "__main__":
    main()
