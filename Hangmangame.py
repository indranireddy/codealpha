import random
import tkinter as tk
from tkinter import messagebox

def get_random_word():
    words = ["python", "hangman", "challenge", "programming", "developer"]
    return random.choice(words)

def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   -----
                   |   |
                   O   |
                  /|\\  |
                  / \\  |
                       |
                ---------
                """,
                # head, torso, both arms, and one leg
                """
                   -----
                   |   |
                   O   |
                  /|\\  |
                  /    |
                       |
                ---------
                """,
                # head, torso, and both arms
                """
                   -----
                   |   |
                   O   |
                  /|\\  |
                       |
                       |
                ---------
                """,
                # head, torso, and one arm
                """
                   -----
                   |   |
                   O   |
                  /|   |
                       |
                       |
                ---------
                """,
                # head and torso
                """
                   -----
                   |   |
                   O   |
                   |   |
                       |
                       |
                ---------
                """,
                # head
                """
                   -----
                   |   |
                   O   |
                       |
                       |
                       |
                ---------
                """,
                # initial empty state
                """
                   -----
                   |   |
                       |
                       |
                       |
                       |
                ---------
                """
    ]
    return stages[tries]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.config(bg="#F0F0F0")
        self.word = get_random_word()
        self.word_completion = "_" * len(self.word)
        self.guessed = False
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6

        self.create_widgets()

    def create_widgets(self):
        self.hangman_label = tk.Label(self.root, text=display_hangman(self.tries), font=("Courier", 20), justify="left", bg="#F0F0F0")
        self.hangman_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.word_label = tk.Label(self.root, text=self.word_completion, font=("Courier", 20), bg="#F0F0F0")
        self.word_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.guess_entry = tk.Entry(self.root, font=("Courier", 20))
        self.guess_entry.grid(row=2, column=0, padx=10, pady=10)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.guess, font=("Courier", 20), bg="#4CAF50", fg="white", activebackground="#45a049")
        self.guess_button.grid(row=2, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game, font=("Courier", 20), bg="#f44336", fg="white", activebackground="#e57373")
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                messagebox.showinfo("Hangman", f"You already guessed the letter {guess}")
            elif guess not in self.word:
                messagebox.showinfo("Hangman", f"{guess} is not in the word.")
                self.tries -= 1
                self.guessed_letters.append(guess)
            else:
                messagebox.showinfo("Hangman", f"Good job, {guess} is in the word!")
                self.guessed_letters.append(guess)
                word_as_list = list(self.word_completion)
                indices = [i for i, letter in enumerate(self.word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.word_completion = "".join(word_as_list)
                if "_" not in self.word_completion:
                    self.guessed = True
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess in self.guessed_words:
                messagebox.showinfo("Hangman", f"You already guessed the word {guess}")
            elif guess != self.word:
                messagebox.showinfo("Hangman", f"{guess} is not the word.")
                self.tries -= 1
                self.guessed_words.append(guess)
            else:
                self.guessed = True
                self.word_completion = self.word
        else:
            messagebox.showinfo("Hangman", "Not a valid guess.")

        self.hangman_label.config(text=display_hangman(self.tries))
        self.word_label.config(text=self.word_completion)

        if self.guessed:
            messagebox.showinfo("Hangman", "Congrats, you guessed the word! You win!")
            self.reset_game()
        elif self.tries == 0:
            messagebox.showinfo("Hangman", f"Sorry, you ran out of tries. The word was {self.word}. Maybe next time!")
            self.reset_game()

    def reset_game(self):
        self.word = get_random_word()
        self.word_completion = "_" * len(self.word)
        self.guessed = False
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6
        self.hangman_label.config(text=display_hangman(self.tries))
        self.word_label.config(text=self.word_completion)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
