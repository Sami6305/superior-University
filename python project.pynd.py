import json
import time
import random  # Added import for random

# Base class for User
class User:
    def __init__(self, username):
        self.__username = username 
        self.__results = []  
        self.high_score = 0  

    def add_result(self, result):
        self.__results.append(result)

    def get_results(self):
        return [{"username": self.__username, "result": result} for result in self.__results]

    def update_high_score(self, wpm):
        if wpm > self.high_score:
            self.high_score = wpm
            print(f"New High Score: {self.high_score} WPM!")

# Class for Typing Test
class TypingTest:
    def __init__(self, sentences):
        self.sentence_list = sentences
        self.start_time = 0
        self.end_time = 0
        self.typed_text = ""
        self.original_text = ""

    def start_test(self):
        self.original_text = random.choice(self.sentence_list)
        print(f"Type the following: \n{self.original_text}")
        self.start_time = time.time()

    def end_test(self, user_input):
        self.end_time = time.time()
        self.typed_text = user_input

    def calculate_speed(self):
        time_taken = self.end_time - self.start_time  # in seconds
        words = len(self.typed_text.split())
        wpm = (words / time_taken) * 60  # Words per minute
        return round(wpm, 2)

    def calculate_accuracy(self):
        original_words = self.original_text.split()
        typed_words = self.typed_text.split()
        correct_words = sum(1 for o, t in zip(original_words, typed_words) if o == t)
        accuracy = (correct_words / len(original_words)) * 100
        return round(accuracy, 2)

    def display_result(self):
        wpm = self.calculate_speed()
        accuracy = self.calculate_accuracy()
        print(f"\nResults:\nWords per minute (WPM): {wpm}\nAccuracy: {accuracy}%")
        return wpm, accuracy

# Class for the Typing Speed Test Application
class TypingSpeedApp:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)  # Changed to use User class
            print(f"User  '{username}' added.")
        else:
            print(f"User  '{username}' already exists.")

    def start_typing_test(self, username):
        if username in self.users:
            test = TypingTest(sentences)
            test.start_test()
            typed_input = input("\nStart typing: ")
            test.end_test(typed_input)
            wpm, accuracy = test.display_result()
            self.users[username].update_high_score(wpm)
            self.users[username].add_result({'wpm': wpm, 'accuracy': accuracy})
        else:
            print(f"User  '{username}' not found. Please add the user first.")

    def save_results_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump({username: user.get_results() for username, user in self.users.items()}, file, indent=4)
        print(f"Results saved to {filename}")

    def load_results_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for username, results in data.items():
                    if username not in self.users:
                        self.users[username] = User(username)  # Changed to use User class
                    for result in results:
                        self.users[username].add_result(result['result'])
                print(f"Results loaded from {filename}")
        except FileNotFoundError:
            print("File not found. Please save results first.")

    def view_results(self):
        for username, user in self.users.items():
            print(f"Results for {username}: {user.get_results()}")

# Main function to run the application
def main():
    global sentences  # Declare sentences as global to use in TypingSpeedApp
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Typing fast requires practice and focus.",
        "Python programming is both fun and educational."
    ]
    
    app = TypingSpeedApp()

    while True:
        action = input("Choose an action: add user (a ), start test (t), save results (s), load results (l), view results (v), or exit (e): ").lower()

        if action == 'a':
            username = input("Enter the username: ")
            app.add_user(username)

        elif action == 't':
            username = input("Enter the username to start the test: ")
            app.start_typing_test(username)

        elif action == 's':
            filename = input("Enter filename to save results (e.g., typing_results.json): ")
            app.save_results_to_file(filename)

        elif action == 'l':
            filename = input("Enter filename to load results (e.g., typing_results.json): ")
            app.load_results_from_file(filename)

        elif action == 'v':
            app.view_results()

        elif action == 'e':
            print("Exiting the Typing Speed Test App.")
            break

        else:
            print("Invalid action. Please try again.")

main()