import getpass
import os
import platform
import random

# Function to clear screen
def clearScreen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Function to save user data to file
def saveUserData(username, password):
    try:
        with open('users.txt', 'a') as file:
            file.write(f"{username}:{password}\n")
        print("Registration successful!")
    except Exception as e:
        print(f"Error saving user data: {e}")

# Function to register a user
def register():
    try:
        username = input("Enter a username: ")
        if username in loadUserData():
            raise ValueError("Username already exists!")
        password = getpass.getpass("Enter a password: ")
        saveUserData(username, password)
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to load user data from file
def loadUserData():
    users = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                users[username] = password
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading user data: {e}")
    return users

# Function to login a user
def login():
    try:
        users = loadUserData()
        if not users:
            clearScreen()
            raise ValueError("No users registered. Please register first.")
        username = input("Enter your username: ")
        if username not in users:
            clearScreen()
            raise ValueError("Username not found!")
        password = getpass.getpass("Enter your password: ")
        if users[username] == password:
            print("Login successful!")
            return username
        else:
            clearScreen()
            raise ValueError("Incorrect password!")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

# Function to load quiz data from file
def loadQuizData(filename):
    quizzes = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            question = ""
            options = []
            answer = ""
            for line in lines:
                line = line.strip()
                if line:
                    if not question:
                        question = line
                    elif len(options) < 4:
                        options.append(line)
                    else:
                        answer = line
                        quizzes[question] = (options, answer)
                        question = ""
                        options = []
                        answer = ""
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error loading quiz data: {e}")
    return quizzes

# Function to conduct the quiz
def takeQuiz(username, subject, quizzes):
    try:
        score = 0
        questions = list(quizzes.items())
        random.shuffle(questions)
        selectedQuestions = questions[:5]

        for question, (options, correctAnswer) in selectedQuestions:
            while True:
                print(question)
                for option in options:
                    print(option)
                answer = input("Enter your answer (a, b, c, d): ")
                if answer in ['a', 'b', 'c', 'd']:
                    break
                else:
                    clearScreen()
                    print("Invalid input. Please enter one of the options: a, b, c, d.")
            if answer == correctAnswer:
                score += 1

        print(f"You scored {score} out of 5")
        saveResult(username, subject, score, 5)
    except Exception as e:
        print(f"Error during quiz: {e}")

# Function to save quiz result
def saveResult(username, subject, score, total):
    try:
        with open('results.txt', 'a') as file:
            file.write(f"{username}:{subject}:{score}/{total}\n")
    except Exception as e:
        print(f"Error saving result: {e}")

# Function to view user results
def viewResults(username):
    try:
        with open('results.txt', 'r') as file:
            results = [line.strip() for line in file if line.startswith(username)]
        if results:
            print(f"Results for {username}:")
            for result in results:
                print(result)
        else:
            print("No results found for the user.")
    except FileNotFoundError:
        print("No results found.")
    except Exception as e:
        print(f"Error loading results: {e}")

# Main function
def main():
    subjects = {
        "1": "Python",
        "2": "C++",
        "3": "Java"
    }
    subjectFiles = {
        "1": "pythonQuiz.txt",
        "2": "cppQuiz.txt",
        "3": "javaQuiz.txt"
    }

    loggedInUser = None
    while True:
        try:
            print("1. Register")
            print("2. Login")
            print("3. Take Quiz")
            print("4. View Results")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                register()
            elif choice == '2':
                loggedInUser = login()
                if loggedInUser:
                    print(f"Welcome, {loggedInUser}!")
                    while True:
                        print("1. Take Quiz")
                        print("2. View Results")
                        print("3. Logout")
                        subChoice = input("Enter your choice: ")
                        if subChoice == '1':
                            print("Choose a subject for the quiz:")
                            for key, subject in subjects.items():
                                print(f"{key}. {subject}")
                            subjectChoice = input("Enter your choice: ")

                            if subjectChoice in subjectFiles:
                                filename = subjectFiles[subjectChoice]
                                quizzes = loadQuizData(filename)
                                if quizzes:
                                    takeQuiz(loggedInUser, subjects[subjectChoice], quizzes)
                                else:
                                    print("No quizzes found.")
                            else:
                                clearScreen()
                                print("Invalid choice. Please try again.")
                        elif subChoice == '2':
                            viewResults(loggedInUser)
                        elif subChoice == '3':
                            print("Logging out...")
                            break
                        else:
                            clearScreen()
                            print("Invalid choice. Please try again.")
            elif choice == '3':
                if loggedInUser:
                    print("Choose a subject for the quiz:")
                    for key, subject in subjects.items():
                        print(f"{key}. {subject}")
                    subjectChoice = input("Enter your choice: ")

                    if subjectChoice in subjectFiles:
                        filename = subjectFiles[subjectChoice]
                        quizzes = loadQuizData(filename)
                        if quizzes:
                            takeQuiz(loggedInUser, subjects[subjectChoice], quizzes)
                        else:
                            print("No quizzes found.")
                    else:
                        clearScreen()
                        print("Invalid choice. Please try again.")
                else:
                    clearScreen()
                    print("Please login first.")
            elif choice == '4':
                if loggedInUser:
                    viewResults(loggedInUser)
                else:
                    clearScreen()
                    print("Please login first.")
            elif choice == '5':
                print("Exiting...")
                break
            else:
                clearScreen()
                raise ValueError("Invalid choice. Please try again.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()