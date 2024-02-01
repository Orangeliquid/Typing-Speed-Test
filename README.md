# Typing Speed Test

## Overview
This Python application is a Typing Speed Test GUI built using Tkinter. Users can test their typing speed by typing a randomly generated set of words within a given time frame. The top score is stored in the words.txt file.

## Features
- User-friendly Interface: The GUI provides a clean and intuitive interface for users to take the typing speed test.
- High Score Tracking: The highest words per minute (WPM) score is stored in the words.txt file. The user's current WPM is displayed in real-time during the test.
- Colorful Design: The application features an orange color scheme, and the color blue is used to highlight correctly typed words.
- Help and About Sections: Users can access helpful information and details about the application's creator through the "Help" and "About" buttons.

## How to Use
- Click on the text box, once you start typing the timer will begin.
- Type the words starting from the top left of the paragraph.
- Press the spacebar after typing each word to move to the next.
- The timer runs for 60 seconds to determine the user's typing speed.
- Use the "Reset" button to restart the test and timer.
- The fastest WPM will be recorded in `~words.txt`.

## Screenshots
![TST_1](https://github.com/Orangeliquid/Typing-Speed-Test/assets/127478612/2a62301b-3b8b-496e-ba3f-a0245c7c1ac6)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Orangeliquid/typing-speed-test.git
   ```
2. Navigate to the project directory:
   ```bash
   cd typing-speed-test
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Run the Application
   ```bash
   python typing_speed_test.py
   ```
- Ensure you have Python installed on your machine.

## Dependencies
- Tkinter: Used for the graphical user interface.
- PIL: Python Imaging Library for working with images.

## License
This project is licensed under the [MIT License](LICENSE.txt).
  
