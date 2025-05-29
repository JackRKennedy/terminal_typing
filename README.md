# Typing Test Project

A simple and interactive command-line typing test application, built using Python. It fetches a random Wikipedia page summary as the sentence to type. The user-friendly interface ensures that accented characters in the sentence can be typed without accents and still be considered correct.

---

## Features

- **Random Sentence Generation**:
    - Uses the Wikipedia API to fetch a sentence from a randomly selected page.
- **Interactive Typing Test**:
    - The application runs in your terminal using `curses`. It provides a clean interface for typing and real-time validation of input.
- **Accent-Aware Typing**:
    - Accented characters like `é`, `ñ`, etc., can be typed as their basic versions (`e`, `n`) without penalising the user.
- **User Feedback**:
    - Provides real-time feedback while typing to indicate if the input is correct so far or if there’s a mistake.
- **Customisable & Lightweight**:
    - All logic is encapsulated in Python code without additional dependencies beyond `curses` and `requests`.

---

## Requirements

- Python **3.13.3**
- Modules:
    - `requests`: For making API calls to fetch random Wikipedia summaries.
    - `curses`: For building the terminal user interface (comes pre-installed with Python in most cases).
    - `unicodedata`: For handling accented characters (comes with the Python standard library).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/JackRKennedy/terminal_typing>
   cd typing-test
   ```

2. **Set Up Dependencies**:
   If you don’t already have `requests` installed, install it using pip:
   ```bash
   pip install requests
   ```

3. **Configuration (Optional)**:
    - No additional configurations are required other than an internet connection to make the API calls. Simply run the program!

---

## How to Run the Project

1. Navigate to the project directory:
   ```bash
   cd typing-test
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Follow the on-screen instructions:
    - The app will display a random sentence from a Wikipedia page.
    - You are required to type it correctly (accented characters may be typed without accents).
    - The app provides feedback while typing and at the end of the test.

---

## Application Details

### Overview of the Application Flow

1. **Welcome Screen**:
    - Displays a welcome message, basic instructions, and waits for the user to press any key to begin.

2. **Typing Test Screen**:
    - A random sentence (Wikipedia summary) is displayed for the user to type.
    - As the user types, their input is compared with the target sentence.
    - Backspace support is available to correct mistakes.

3. **Accent Handling**:
    - Behind the scenes, accented characters are converted to their base forms (e.g., `é` to `e`).
    - Input is validated against the accent-free version of the sentence.

4. **Feedback**:
    - If the user’s input matches the target sentence (up to the last character typed), they are allowed to continue.
    - If there’s a mismatch, an error message is shown.
    - At the end of the typing test, users are informed whether they successfully typed the sentence.

---

### Code Structure

- **`get_sentence`**:
    - Fetches a random Wikipedia page summary and provides both the title and the sentence for the typing test.

- **`remove_accents`**:
    - Converts accented characters to their unaccented counterparts using `unicodedata`.

- **`typing_test`**:
    - Main function implementing the typing test using the `curses` module.
    - Displays the sentence, captures user input, validates it in real-time, and provides interactive feedback.

- **`main.py`**:
    - Entry point of the program, wraps the `typing_test` function with `curses.wrapper`.

---

### Error Handling

- **API Errors**:
    - If the Wikipedia API fails for any reason, an error message ("Failed to retrieve data") is displayed in the application.

- **Curses Cleanup**:
    - The program ensures proper cleanup of the terminal state using `curses.endwin` in case of any exception.

---

## Example Run

- **Welcome Screen**:
  ```plaintext
  -----------------------------------
        Welcome to the typing test
  -----------------------------------
    Press any key to begin
  ```

- **Typing Test**:
  ```plaintext
  Title: Café (Wikipedia Summary)
  Sentence to type: Cafe is a place to enjoy.

  Your input: 
  (Type the sentence above. Accented characters can be typed without accents.)
  ```

- **Real-Time Feedback**:
  ```plaintext
  Your input: Cafe is a
  Your input is incorrect! Try again.
  ```

- **Final Message**:
  ```plaintext
  Congrats! Your input is correct.
  ```

---

## Known Limitations

- **Terminal Compatibility**:
    - The `curses` module may not work perfectly on all terminal emulators, it is better to run this software using a unix based terminal system, or a Ubuntu instance on WSL if on Windows
    - For issues related to colours or input handling, you may need to tweak the terminal settings.

- **Lengthy Sentences**:
    - Some Wikipedia summaries may be overly large for the terminal window and as a result they are truncated and end in "..." -> this will be addressed in a future update

---

### For Developers

#### Modifying the Sentence Source
If you want to use an alternative source for the sentences:
- Replace the `get_sentence` function with a new data-fetching function.
- Add a local DB or spreadsheet to pull sentences from, this consideration is also in the works for a future update to optimise speed

#### Debugging Issues with `curses`
- Use print statements sparingly, as `curses` suppresses them by default.
- Wrap the entire terminal logic with `curses.wrapper`.

---

## Contributing

We welcome suggestions and contributions to enhance this typing test project. Feel free to:
- Fork the repository and submit pull requests.
- Report issues or suggest features.

For any questions, open a discussion or reach out!

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it as needed.