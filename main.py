"""
Typing Test
A terminal-based typing test tool that measures your typing speed (WPM) and highlights accuracy.

Features:
- Interactive terminal-based typing test
- Measures Words Per Minute (WPM)
- Colored display for user feedback

Content:
- Using the free wikipedia API, the program pulls a random page summary from the wikipedia website for you to type
- This means that you are typing real-world sentences which can contain all alphanumeric characters and symbols
- It also means that there is no control over how long or how short the page summary is, so each test is different
- Please also note that the content could possibly give you a page summary of something you disagree with or are offended by
- In such case, please use the reload button to get a new page summary (CTRL+R)

TODO:
- allow command line arguments to be passed to change the difficulty of the test
- allow cla's of -e, -m and -h to be passed for easy, medium and hard modes respectively
- each mode will trigger a calculation on the API call to display content of a maximum number of words
- this will be unlimited in the case of hard and only short sentences in the case of easy and medium(slightly longer)
- we will do a mass call on the api and fill a list of sentences that could be used, and calculate the shorterst for the easy etc
- could also find a source online of a normal distribution of all english words where easy compares
- the sentence to the distribution of english words and will give a page summary with mostly common words
"""

import pygame # for asynchronous sound
import curses  # Terminal formatting module
import time  # For WPM calculation
import requests # for wiki api call
import unicodedata # for normalising page summaries so that accents over viwels can be ignored

def split_sentence(input_str: str, terminal_width: int) -> list[str]:
    """
    Split a sentence into smaller chunks to fit in the terminal,
    ensuring that words are not broken across lines.
    Args:
        input_str: The input sentence to split.
        terminal_width: The width of the terminal in characters.
    Returns:
        A list of sentence chunks (lines).
    """
    buffer_size = 15  # arbitrary safe value for padding from window edges
    safe_width = max(terminal_width - buffer_size, 1)  # allow at least small gap

    words = input_str.split()  # Split by whitespace and handle multiple spaces
    if not words:
        return []

    sentence_list = []
    current_line_words = []

    for word in words:
        if not current_line_words:
            # If the current line is empty, always add the first word
            # (even if it's longer than safe_width, it will form its own line)
            current_line_words.append(word)
        else:
            # Check if the current word can be added to the existing line
            # +1 for the space character
            if len(" ".join(current_line_words)) + 1 + len(word) <= safe_width:
                current_line_words.append(word)
            else:
                # Word doesn't fit, finalise current line
                sentence_list.append(" ".join(current_line_words))
                # Start a new line with the current word
                current_line_words = [word]

    # Add the last constructed line
    if current_line_words:
        sentence_list.append(" ".join(current_line_words))

    # Handle the case where the input string was empty or only whitespace,
    # and split_sentence produced a list with one empty string.
    if len(sentence_list) == 1 and not sentence_list[0]:
        return []

    return sentence_list


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_sentence():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "No title found")
        sentence = data.get("extract", "No summary found")
        return title, sentence
    else : return "Error", "Failed to retrieve data"

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
    title, sentence = get_sentence() # unpack sentence function to return title and summary
    sentence = remove_accents(sentence) # remove accents from summary
    if title == "Error":
        stdscr.clear()
        stdscr.addstr(2, 10, "API request failed. Please try again.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()  # Wait for user input before retrying
        return  # Exit the function before running the rest

    # initialise pygame components
    pygame.mixer.init()
    good_sound = pygame.mixer.Sound("sounds/typewriter_key.mp3")
    bad_sound = pygame.mixer.Sound("sounds/clank1-91862.mp3")

    word_count = len(sentence.split(" "))  # Count words for WPM calculation
    user_input = ""
    index = 0  # Current position in the sentence
    start_time = None  # Timing starts when the first character is typed

    # Get screen dimensions for proper positioning
    height, width = stdscr.getmaxyx()

    # # Ensure sentence isn't too long for the terminal
    # if len(sentence) > width - 10:
    #     sentence = sentence[:width - 15] + "..."

    # Ensure no negative position values
    title_x = max((width - len(title)) // 2, 0)
    title_y = max(height // 2 - 2, 0)
    sentence_x = max((width - len(sentence)) // 2, 0)
    sentence_y = max(height // 2, 0)

    # Display the title in the centre-top of the screen
    stdscr.addstr(title_y, title_x, title.upper(), curses.A_BOLD)

    # Display a sentence in the centre of the screen
    # stdscr.addstr(sentence_y, sentence_x, sentence)

    sentence_list = split_sentence(sentence, width)
    for index, line in enumerate(sentence_list):
        start_x = max((width - len(line)) // 2, 0)
        stdscr.addstr(sentence_y + index, start_x, line)

    # need new variable to check user progress in sentence
    current_line = 0
    current_pos = 0

    user_input = [""] * len(sentence_list) # empty initially

    stdscr.refresh()

    # Loop through the sentence until the user finishes
    while current_line < len(sentence_list):
        # Position the cursor at the start of the sentence
        stdscr.move(sentence_y + current_line, max((width - len(sentence_list[current_line]))//2 + current_pos, 0))

        key = stdscr.getch()  # Capture user key press
        char = chr(key) if 32 <= key <= 126 else None  # 'Normalise' key input

        if start_time is None:
            start_time = time.time()  # Start the timer on the first key press

        if char: # regular expected alphanumeric character
            if current_pos < len(sentence_list[current_line]):
                if char == sentence_list[current_line][current_pos]:
                    # correct key entered, advance curor and updater user input
                    good_sound.play()
                    stdscr.addstr(sentence_y + current_line, (width - len(sentence_list[current_line])) // 2 + current_pos, char, curses.color_pair(2))  # Highlight green
                    user_input[current_line] += char
                    current_pos += 1
                else:
                    # incorrect key entered, advance curor and update user input
                    bad_sound.play()
                    stdscr.addstr(sentence_y + current_line, (width - len(sentence_list[current_line])) // 2 + current_pos, sentence_list[current_line][current_pos], curses.color_pair(3))  # Highlight red

                # if we reached the end of the line
                if current_pos == len(sentence_list[current_line]):
                    # move to next line and reset cursor position
                    current_line += 1
                    current_pos = 0

        elif key in (8, 127):  # Backspace
            if current_pos > 0:
                current_pos -= 1
                user_input[current_line] = user_input[current_line][:-1]  # Remove last character
                # Erase character on screen
                stdscr.addstr(sentence_y + current_line,
                              (width - len(sentence_list[current_line])) // 2 + current_pos,
                              " ", curses.color_pair(3))

            elif current_line > 0:
                # Move back to the end of the previous line
                current_line -= 1
                current_pos = len(user_input[current_line])

        elif key == 18: # ASCII CTRL+R
            # refresh the API call and start again
            stdscr.clear()
            typing_test(stdscr)

        # Refresh the screen
        stdscr.refresh()

    # break out of while loop when sentence is completed
    end_time = time.time()

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
    stdscr.clear()
    clean_up_curses(stdscr)
    return


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

        try:
            typing_test(stdscr)
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(2, 10, "An error occurred during the test. Please try again.", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()

    except Exception as e:
        print(f"Encountered error: {e}")  # Print errors outside curses mode
    finally:
        clean_up_curses(stdscr)  # Ensure terminal is restored
        pygame.mixer.quit()
        pygame.quit()


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
            # curses.endwin() -> this should be handled by the wrapper function
        except curses.error:
            pass


if __name__ == '__main__':
    # Initialise curses wrapper which manages setup and teardown
    curses.wrapper(main)