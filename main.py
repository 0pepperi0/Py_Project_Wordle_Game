import pathlib
import random
from string import ascii_letters, ascii_uppercase
from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))


def main():

    global indx
    word = get_random_word()

    guesses = ["_" * 5] * 6

    for indx in range(6):
        refresh_page(headline=f"Guess {indx + 1}")

        demonstrate_guesses(guesses, word)
        guesses[indx] = guess_word(previous_guesses=guesses[:indx])
        if guesses[indx] == word:
            break

    finish_game(guesses, word, guessed_correctly=(guesses[indx] == word))


def get_random_word():
    wordlist = pathlib.Path("word_list.txt")
    if words := list(
        word.upper()
        for word in wordlist.read_text(encoding="utf-8").split("\n")
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    ):
        return random.choice(words)
    else:
        console.print("No words of length 5 in the word list", style="warning")
        raise SystemExit()




def finish_game(guesses, word, guessed_correctly):
    refresh_page(headline="Game over")
    demonstrate_guesses(guesses=guesses, word=word)

    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct! The word was {word}[/]")
    else:
        console.print(f"\n[bold white on red]Wrong! The word was {word}[/]")


def demonstrate_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
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
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify="center")

    console.print("\n" + "".join(letter_status.values()), justify="center")


def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()
    if guess in previous_guesses:
        console.print(f"You have already tried the word {guess}. Try another.", style="warning")
        return guess_word(previous_guesses)

    if len(guess) != 5:
        console.print(f"The word should be 5 letters", style="warning")
        return guess_word(previous_guesses)

    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f"The guess has invalid symbol {invalid} in it. Try on more time", style="warning")
        return guess_word(previous_guesses)

    return guess


if __name__ == "__main__":
    main()
