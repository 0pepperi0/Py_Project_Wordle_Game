import pathlib
import random
from string import ascii_letters
from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))

def main():

    word = get_random_word()

    guesses = ["_" * 5] * 6

    for indx in range(6):
        refresh_page(headline=f"Guess {indx + 1}")

        demonstrate_guesses(guesses, word)
        guesses[indx] = input(f"\nGuess {indx + 1}: ").upper()
        if guesses[indx] == word:
            break

    else:
        finish_game(word)


def get_random_word():
    wordlist = pathlib.Path("word_list.txt")
    words = list(
        word.upper()
        for word in wordlist.read_text(encoding="utf-8").split("\n")
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    )
    word = random.choice(words)
    return word


def finish_game(word):
    print(f"The word was {word}")


def demonstrate_guesses(guesses, word):
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")

        console.print("".join(styled_guess), justify="center")
def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


if __name__ == "__main__":
    main()
