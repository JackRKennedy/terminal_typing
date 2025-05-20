"""
Creating a very simple typing test in the terminal for personal use
Nothing fancy but iteratively adding to the project

Step 1: Working terminal that prints to the screen every letter you type, times you and measures wpm

Step 1: Fancier overlay where the sentence is already on screen in one colour and each letter fills to a different colour when typed

Step 3: UI clean up with timers, titles, padding on the ui, potentially some better background etc

Step 4: Feature to include an option on how many sentences to type, integration with API to pull quotes from books etc
"""

if __name__ == '__main__':

    print("Welcome to the Terminal Typing Test:\n")

    sentence : str = "the quick brown fox jumps over the lazy dog"

    print(f"{sentence}\n")
