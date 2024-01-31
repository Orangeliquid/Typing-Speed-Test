import tkinter as tk
from tkinter import Entry, END, messagebox
from PIL import ImageTk, Image
import random
import time


class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_color = self.cget('fg')
        self.bind("<FocusIn>", self.on_entry_focus_in)
        self.bind("<FocusOut>", self.on_entry_focus_out)
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
        self.center_text()

    def on_entry_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self.config(fg=self.default_color)
            self.center_text()

    def on_entry_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
            self.center_text()

    def center_text(self):
        # Set justify option to center
        self.config(justify="center")


def help_message():
    messagebox.showinfo(title="Help",
                        message="Welcome to Help!\n\nFirst: Click the text box, once clicked the timer will start\n"
                                "\nSecond: Type the words starting from the top left of the paragraph\n"
                                "\nThird: When you type the word and hit space the text you typed will disappear\n"
                                "\nFinally: 60 seconds to see how many words you can type!\n"
                                "\npsst - The restart button will reset the timer and words above!\n"
                                "\nTry to get on the Highscore!"
                        )


def about_message():
    messagebox.showinfo(title="About this app",
                        message="This is my take on a typing speed test. I utilize the color Orange because I truly"
                                " love the color. I am a new software developer that enjoys learning by doing. "
                                "Feel free to use this app, whether as a typing speed test, or build your own"
                                " rendition with my app as a starting point! Enjoy!"
                        )


class TypingSpeedTest:
    """
        TypingSpeedTest class for a typing speed test application.

        Attributes:
            window (tkinter.Tk): The main window of the application.
            words (list): A list of words used in the typing test.
            sample_text (str): A sample text generated for the typing test.
            sample_text_list (list): The sample text split into a list of words.
            words_per_line (int): Number of words per line in the display.
            wpm_score (int): The highscore of words per minute.
            start_time (float): The timestamp when the typing test starts.
            timer_running (bool): Flag indicating whether the timer is running.
            remaining_time (int): The remaining time in seconds.
            cpm (int): Characters per minute.
            wpm (int): Words per minute.
            word_index (int): Index of the current word.
            current_word (str): Current word being typed.
            entered_words (list): List to store entered words.
            word_colors (list): List to store colors for each word based on correctness.
        """
    WORDS_PER_LINE = 7

    def __init__(self, window_start):
        # Window creation and config
        self.window = window_start
        self.window.title("Typing Speed Test")
        self.window.config(bg="#FFDEAD")

        # Get the words from words.txt file
        self.words_per_line = TypingSpeedTest.WORDS_PER_LINE
        try:
            with open('words.txt', 'r') as file:
                self.words = file.read().split()
                self.words = [word.lower() for word in self.words if 3 <= len(word) <= 6]
                self.sample_text = ' '.join(random.sample(self.words, 100))
                self.sample_text_list = self.sample_text.split()
        except FileNotFoundError:
            # Handle the case where 'words.txt' is not found
            messagebox.showerror("Error", "The 'words.txt' file is not found.")
            # Raise an error to indicate that the app cannot proceed without 'words.txt'
            raise FileNotFoundError("The 'words.txt' file is required for the application.")
        except IOError as e:
            # Handle other IO-related errors
            messagebox.showerror("Error", f"Error reading 'words.txt': {e}")
            raise IOError(f"Error reading 'words.txt': {e}")
        except Exception as e:
            # Handle other unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

        try:
            with open('high_score.txt', 'r') as file:
                self.wpm_score = int(file.read())
        except FileNotFoundError:
            self.wpm_score = 0

        # initializing start_time, time_running, remaining_time, clicks per minute
        self.start_time = None
        self.timer_running = False
        self.remaining_time = 60
        self.cpm = 0
        self.wpm = 0

        # Logo creation and grid
        self.alien_logo_img = ImageTk.PhotoImage(Image.open("orange_alien.png"))
        self.logo_canvas = tk.Canvas(width=120, height=120, bg="#FFDEAD", highlightthickness=0)
        self.logo_canvas.create_image(60, 60, image=self.alien_logo_img)
        self.logo_canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Highscore label and grid
        self.hs_label = tk.Label(text="Highscore:", bg="#FFDEAD", font="Futura", width=8, anchor="w")
        self.hs_label.grid(row=1, column=0)
        self.hs_display = tk.Message(text=self.wpm_score, bg="#FFDEAD", font="Futura", highlightbackground="#ADCEFF",
                                     highlightthickness=4, width=50, anchor="w")
        self.hs_display.grid(row=1, column=1)

        # Clicks per minute label and grid
        self.cpm_label = tk.Label(text="Last CPM:", bg="#FFDEAD", font="Futura", width=8, anchor="w")
        self.cpm_label.grid(row=2, column=0)
        self.cpm_display = tk.Message(text=self.cpm, bg="#FFDEAD", font="Futura", highlightbackground="#ADCEFF",
                                      highlightthickness=4, width=50, anchor="w")
        self.cpm_display.grid(row=2, column=1)

        # Words per minute label and grid
        self.wpm_label = tk.Label(text="Last WPM:", bg="#FFDEAD", font="Futura", width=8, anchor="w")
        self.wpm_label.grid(row=3, column=0)
        self.wpm_display = tk.Message(text=self.wpm, bg="#FFDEAD", font="Futura",
                                      highlightbackground="#ADCEFF", highlightthickness=4, width=50, anchor="w")
        self.wpm_display.grid(row=3, column=1)

        # Time label and grid
        self.time_display = tk.Message(text=self.remaining_time, bg="#FFDEAD", font=("Futura", 25), width=50, pady=5,
                                       anchor="s")
        self.time_display.grid(row=0, column=5, rowspan=3)
        self.time_label = tk.Label(text='Time left: ', bg="#FFDEAD", font=("Futura", 15), width=10, pady=5, anchor="n")
        self.time_label.grid(row=1, column=5, rowspan=1)

        # Reset button and grid
        self.reset_btn = tk.Button(text='Reset', width=8, bg="#ADCEFF", font="Futura", command=self.reset_test)
        self.reset_btn.grid(row=5, column=5, rowspan=2, padx=10)

        # Text box and grid
        self.text = tk.Text(height=5, width=50, wrap="none", font=("Arial", 20), spacing1=8, spacing2=12, spacing3=12)
        self.text.grid(row=0, column=2, columnspan=3, rowspan=5, pady=20, padx=10)

        self.insert_formatted_text()
        self.center_text()

        # Typing box for user creation and grid
        self.type_entry = PlaceholderEntry(self.window, placeholder='Type here to start', color='black',
                                           font=("Futura", 25), width=45, bg='#FFDEAD')
        self.type_entry.config(highlightbackground="#ADCEFF", highlightthickness=3)
        self.type_entry.grid(row=5, column=3, rowspan=2, padx=10, pady=15)

        # Help button and grid
        self.help_button = tk.Button(text="Help", width=8, bg="#ADCEFF", font="Futura", command=help_message)
        self.help_button.grid(row=5, column=0, padx=10)

        # About button creation and grid
        self.about_button = tk.Button(width=8, text="About", bg="#ADCEFF", font="Futura", command=about_message)
        self.about_button.grid(row=6, column=0, pady=10, padx=10)

        # Initializing word index and current word plus list creation
        self.word_index = 0  # Index of the current word
        self.current_word = ""  # Current word being typed
        self.entered_words = []  # List to store entered words
        self.word_colors = []

        # Bind events to entry widget
        self.type_entry.bind("<KeyRelease>", self.on_key_release)
        self.type_entry.bind("<Return>", self.on_return_or_space_pressed)
        self.type_entry.bind("<space>", self.on_return_or_space_pressed)
        self.type_entry.bind("<BackSpace>", self.on_backspace_pressed)

        # Bind the highlight_current_word method to the Map event
        self.window.after(100, self.highlight_current_word)

    def reset_test(self):
        # Enable the Entry
        self.text.config(state="normal")
        self.type_entry.config(state="normal")

        # Reset the words and timer
        self.sample_text = ' '.join(random.sample(self.words, 100))  # This picks 100 random words from words.txt
        self.remaining_time = 60
        self.word_index = 0
        self.entered_words = []
        self.word_colors = []
        self.sample_text_list = self.sample_text.split()

        # Update the display
        self.text.delete("1.0", "end")
        self.insert_formatted_text()
        self.center_text()
        self.update_display()

        # Reset the timer-related variables
        self.start_time = None
        self.timer_running = False
        self.cpm = 0
        self.wpm = 0
        self.update_timer()

        # Reset the Entry to its initial state with the placeholder
        self.type_entry.delete(0, END)

    def insert_formatted_text(self):
        words = self.sample_text.split()
        for i in range(0, len(words), self.words_per_line):
            line = ' '.join(words[i:i + self.words_per_line])
            self.text.insert(END, line + '\n')

    def center_text(self):
        self.text.tag_configure("center", justify="center")
        self.text.tag_add("center", "1.0", "end")

    def on_key_release(self, event):
        # Check if the entry is disabled (blocked)
        if self.type_entry.cget("state") == "disabled":
            return

        # Check if the timer is running before updating
        if not self.timer_running:
            self.start_timer()

        # Update the highlighting with color based on correctness
        self.window.after(100, self.update_highlighting)  # Schedule the next update

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.window.after(1000, self.update_timer)

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.remaining_time = max(60 - int(elapsed_time), 0)
            self.time_display.config(text=self.remaining_time)
            if self.remaining_time > 0 and self.timer_running:
                self.window.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.type_entry.config(state="disabled")
                self.display_result()

    def display_result(self):
        # calculating clicks per minute
        for typed_word, text_word in zip(self.entered_words, self.sample_text.split()):
            for typed_letter, text_letter in zip(typed_word, text_word):
                if typed_letter == text_letter:
                    self.cpm += 1

        # calculating words per minute
        self.wpm += sum(1 for entered_word in self.entered_words if entered_word in self.sample_text_list)

        # removing words from text box and inserting end message
        self.text.delete("1.0", "end")
        self.text.insert(END, f'Your CPM is {self.cpm} and your WPM is {self.wpm}\n')

        # if the wpm is higher than HS then write to the txt document to update HS
        if self.wpm > self.wpm_score:
            self.text.insert(END, '🎉 CONGRATS!! You set a new Word Per Minute Record! 🎉\n')
            with open('high_score.txt', 'w') as file:
                file.write(str(self.wpm))
        else:
            self.text.insert(END, f'Great try! Your fastest WPM is {self.wpm_score}\n')
        self.text.config(state="disabled")

    def update_display(self):
        self.cpm_display.config(text=self.cpm)
        self.wpm_display.config(text=self.wpm)

        # Reading HS text file for current HS
        with open('high_score.txt', 'r') as file:
            self.wpm_score = int(file.read())
        self.hs_display.config(text=self.wpm_score)
        self.time_display.config(text=60)

    def on_return_or_space_pressed(self, event):
        # Move to the next word when Enter or Space is pressed
        self.word_index += 1

        # Remove leading/trailing spaces
        current_entry_text = self.type_entry.get().lower().strip()

        # Append to entered_words only if the entry is not empty
        if current_entry_text:
            self.entered_words.append(current_entry_text)
        if self.sample_text.split()[self.word_index - 1] == current_entry_text:
            self.word_colors.append('blue')
        else:
            self.word_colors.append('red')
        self.current_word = ""

        # Clear the entry
        self.type_entry.delete(0, END)

        # Schedule the next update
        self.window.after(100, self.update_highlighting)
        self.color_the_word()
        if self.word_index % 7 == 0 and self.word_index > 13:
            self.text.yview_scroll(1, "units")

    def on_backspace_pressed(self, event):
        # Handle backspace pressed
        if len(self.type_entry.get()) == 1 and self.word_index > 0:
            # If the entry is empty and there are entered words, go back to the previous word
            self.word_index -= 1
            self.color_the_word(True)
            self.current_word = self.entered_words.pop()
            print("popped word due to backspace pressed")
            self.type_entry.insert(0, self.current_word)

            # Schedule the next update
            self.window.after(100, self.update_highlighting)

    def update_highlighting(self):
        if not self.timer_running:
            return
        # Remove previous highlighting
        self.text.tag_remove("highlight", "1.0", "end")
        for i in range(len(self.sample_text)):
            self.text.tag_remove(f"highlight_letter_{i}", "1.0", "end")

        # Highlight the current word with color based on correctness
        if 0 <= self.word_index < len(self.sample_text.split()):
            current_word = self.sample_text.split()[self.word_index]
            current_text = self.type_entry.get().lower()
            word_start_index = f'{self.text.search(current_word, "1.0", "end-1c", regexp=True)}'

            # Set to the beginning if current word is empty
            if not word_start_index:
                word_start_index = "1.0"
            word_end_index = f"{word_start_index}+{len(current_word)}c"
            self.text.tag_add("highlight", word_start_index, word_end_index)
            self.text.tag_configure("highlight", background="#ADCEFF")
            current_text = current_text.strip()
            for i, (letter_word, letter_text) in enumerate(zip(current_word, current_text)):
                start_index = f'{word_start_index}+{i}c'
                end_index = f"{start_index}+1c"
                tag_name = f"highlight_letter_{i}"

                self.text.tag_add(tag_name, start_index, end_index)

                if letter_word == letter_text:
                    self.text.tag_configure(tag_name, foreground="white")
                else:
                    self.text.tag_configure(tag_name, foreground="red")

    def highlight_current_word(self):
        # Highlight the current word
        if 0 <= self.word_index < len(self.sample_text.split()[0]):
            start_index = self.text.search(self.sample_text.split()[0], "1.0", "end-1c", regexp=True)
            end_index = f"{start_index}+{len(self.sample_text.split()[0])}c"
            self.text.tag_add("highlight", start_index, end_index)

            self.text.tag_configure("highlight", background="#ADCEFF")

    def color_the_word(self, backspace=False):
        if backspace:
            self.word_colors.pop()
            self.text.tag_remove(f"color_letter_{self.word_index}", "1.0", "end")
            return
        for i, color in enumerate(self.word_colors):
            start_index = self.text.search(self.sample_text.split()[i], "1.0", "end-1c", regexp=True)
            end_index = f"{start_index}+{len(self.sample_text.split()[i])}c"
            tag_name = f"color_letter_{i}"

            self.text.tag_add(tag_name, start_index, end_index)
            self.text.tag_configure(tag_name, foreground=color)


if __name__ == '__main__':
    window = tk.Tk()
    typing_speed_test = TypingSpeedTest(window)
    window.mainloop()
