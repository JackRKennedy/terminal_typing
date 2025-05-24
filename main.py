"""
Typing Test
A terminal-based typing test tool that measures your typing speed (WPM) and highlights accuracy.

Features:
- Interactive terminal-based typing test
- Measures Words Per Minute (WPM)
- Colored display for user feedback

Future Plans:
- Add sentence customisation options
- Integrate with external APIs for content
- UI improvements and additional features
"""

import pygame
import curses  # Terminal formatting module
import time  # For WPM calculation

def play_sound(file):
    """
    Play a sound file using pygame.
    Args:
        file: The path to the sound file.
    """
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file)
    sound.play()

def initialize_curses(stdscr):
    """
    Initialise curses settings for terminal interaction.
    Ensures input is captured cleanly and colours are set up.
    """
    stdscr.clear()  # Ensure the terminal screen starts clean

    # Turn off echo mode (characters won't be visible when typed)
    # Enable immediate key reactions and special key handling
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Initialise colour pairs for custom UI elements
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default white text
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # For correct characters
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # For incorrect characters

    # Set the initial screen background colour
    stdscr.bkgd(' ', curses.color_pair(1))


def display_header(stdscr, width, text):
    """
    Display a centered header text at a fixed row.
    Args:
        stdscr: The curses window instance.
        width: Screen's width for centering text.
        text: The header content to display.
    """
    header_x = (width - len(text)) // 2  # Calculate x-position for centre alignment
    stdscr.addstr(2, header_x, text, curses.A_BOLD)


def display_prompt(stdscr, width, text, height):
    """
    Display a centered prompt on the screen.
    Args:
        stdscr: The curses window instance.
        width: Screen's width for alignment.
        text: The prompt message to show.
        height: Screen's height for vertical positioning.
    """
    prompt_x = (width - len(text)) // 2
    prompt_y = height // 2  # Place it in the middle of the screen
    stdscr.addstr(prompt_y, prompt_x, text)


def typing_test(stdscr):
    """
    Main logic for the typing test:
    Handles user interaction, tracks progress, and calculates WPM.
    """
    # Sentence to type and initialise the necessary variables
    sentence = "the quick brown fox jumps over the lazy dog"
    word_count = len(sentence.split(" "))  # Count words for WPM calculation
    user_input = ""
    index = 0  # Current position in the sentence
    start_time = None  # Timing starts when the first character is typed

    # Get screen dimensions for proper positioning
    height, width = stdscr.getmaxyx()

    # Display a sentence in the centre of the screen
    sentence_x = (width - len(sentence)) // 2
    sentence_y = height // 2
    stdscr.addstr(sentence_y, sentence_x, sentence)

    # Position the cursor at the start of the sentence
    stdscr.move(sentence_y, sentence_x)
    stdscr.refresh()

    # Loop through the sentence until the user finishes
    while index < len(sentence):
        key = stdscr.getch()  # Capture user key press

        if start_time is None:
            start_time = time.time()  # Start the timer on the first key press

        if key == ord(sentence[index]):  # Correct character entered
            user_input += chr(key)  # Append character to user input
            # Display character with the correct colour
            stdscr.addch(sentence_y, sentence_x + index, chr(key), curses.color_pair(2))
            play_sound("typewriter_key.mp3")
            index += 1  # Move to the next character

            # If input is complete, calculate results
            if len(user_input) == len(sentence):
                end_time = time.time()

                break
        elif key in (curses.KEY_BACKSPACE, 8):  # Handle backspace functionality
            if index > 0 and user_input[-1] != sentence[index - 1]:  # Allow backspace only on mismatches
                index -= 1  # Move the cursor to the previous position
                user_input = user_input[:-1]  # Remove last entered character

                # Restore original correct character in default colour
                stdscr.addch(sentence_y, sentence_x + index, sentence[index], curses.color_pair(1))
        elif key != ord(sentence[index]):  # Incorrect character entered
            # Highlight incorrect character with a different colour
            stdscr.addch(sentence_y, sentence_x + index, sentence[index], curses.color_pair(3))
            play_sound("clank1-91862.mp3")
            # Keep cursor on the same position for retry
            stdscr.move(sentence_y, sentence_x + index)

        stdscr.refresh()  # Refresh the screen to show updates

    # Show WPM results after the test
    if end_time:
        display_results(stdscr, width, height, word_count, start_time, end_time)


def display_results(stdscr, width, height, word_count, start_time, end_time):
    """
    Calculate and display the final results (WPM and completion message).
    Args:
        stdscr: The curses window instance.
        width:  Screen dimension for positioning.
        height: Screen dimension for positioning.
        word_count: Total words in the test sentence.
        start_time: Timestamp for test start.
        end_time: Timestamp for test end.
    """
    elapsed_time = end_time - start_time  # Total time taken
    wpm = (word_count / elapsed_time) * 60  # Calculate words per minute

    # Prepare result messages
    result_header = "Congratulations and well done on completing the typing test!"
    wpm_result = f"WPM: {wpm:.2f}"  # Display up to 2 decimal places

    # Header and result positioning
    result_header_x = (width - len(result_header)) // 2
    wpm_result_x = (width - len(wpm_result)) // 2

    # Clear screen before showing results
    stdscr.clear()
    stdscr.addstr(2, result_header_x, result_header, curses.A_BOLD)
    stdscr.addstr(height // 2, wpm_result_x, wpm_result, curses.A_BOLD)
    stdscr.refresh()

    # Wait for a key press to exit
    stdscr.getch()


def main(stdscr):
    """
    Main entry point for the program.
    Responsible for initialisation, execution, and UI management.
    """
    try:
        initialize_curses(stdscr)  # Prepare curses settings for the terminal

        # Display welcome interface
        height, width = stdscr.getmaxyx()  # Get terminal dimensions
        display_header(stdscr, width, "Welcome to the Typing Test!")
        display_prompt(stdscr, width, "Press any key to begin...", height)
        stdscr.refresh()
        stdscr.getch()  # Wait for user to press any key to start

        # Clear screen and start typing test
        stdscr.clear()
        typing_test(stdscr)

    except Exception as e:
        print(f"Encountered error: {e}")  # Print errors outside curses mode
    finally:
        clean_up_curses(stdscr)  # Ensure terminal is restored


def clean_up_curses(stdscr):
    """
    Restores the terminal to its original state after curses mode.
    """
    if stdscr:
        try:
            # Reset terminal settings modified by curses
            stdscr.keypad(False)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        except Exception as e:
            print(f"Error during cleanup: {e}")  # Handle cleanup failures


if __name__ == '__main__':
    # Initialise curses wrapper which manages setup and teardown
    curses.wrapper(main)