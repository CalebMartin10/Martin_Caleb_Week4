import json

def load_json_data(json_file):
    try:
        with open(json_file, "r") as file:
            student_data = json.load(file)
    except FileNotFoundError:  # Handles the creation of a new file
        print(f"File does not exist.. Creating file")
        with open(json_file, "x") as file:
            student_data = {}
    except json.decoder.JSONDecodeError:  # this statement is needed so the code can move on if the file contains no data
        print(f"Your JSON file currently has no data in it")
        student_data = {}
    return student_data

def dump_json_data(dictionary, json_file):
    try:
        with open(json_file, "w",) as file:
            json.dump(dictionary, file, indent=4)
            print("Data written to JSON file")
    except IOError:
        print("You did not have proper Authorization to write to file")


grade_data = {  # Used by the gpa functions to calculate grades
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0
}

response_data = {  # Responses in the last bit of this program do not function proeprly unless specified in this way
    "1": "add",
    "2": "update",
    "3": "gpa",
    "4": "generate",
    "5": "exit",
    "6": "all",
    "7": "maj",
    "8": "allgpa",
    "9": "single"
}

def verify_name_input(message):
    """
    Verifies that an input is a string value
    """
    while True:
        try:
            name = input(message)
            verified_name = float(name)
            if isinstance(verified_name, float):
                print("Input must be a word")
        except ValueError:
            return name


def verify_id_input(message) -> str:
    """
    Verifies that an input is a whole number
    """
    while True:
        try:
            id = int(input(message))
            return str(id)
        except ValueError:
            print("Input must be a whole number")


def add_student_record(dictionary):
    """
    Adds a student record into a dictionary
    """
    while True:
        id = verify_id_input("What is the student's ID number? ")
        if id in dictionary:
            print("id is already exists")
            continue
        else:
            break
    name = verify_name_input("What is the student's name? ")
    major = verify_name_input("What is their major? ")
    try:
        dictionary[id] = {"name": name, "major": major, "grades": {}}
    except KeyError:
            print("Dictionary or key does not exist")
    print("Added student to dictionary\n")

    
def update_student_grades(dictionary):
    """
    Updates or adds a student's completed classes and their grade
    """
    while True:
        id = verify_id_input("What is the student's ID number? ")
        try:
            verification = input(f"Is this {dictionary[id]["name"]} the correct student? (Y/N) ").strip().lower()
            if verification == "y" or "yes":
                print("Verification Accepted")
                break
            elif verification == "n" or "no":
                print("Re-input the studen't ID")
            else:
                print("Type in y/yes or n/no")
        except KeyError:
            print("Dictionary or key does not exist")
    course = verify_name_input("What class did they take? ").upper()
    grade = verify_name_input("What grade did they get (A to F)? ").upper()
    try:
        dictionary[id]["grades"].update({course: grade})
    except KeyError:
        print("Key or Dictionary did not exist")
    print("Added grade to dictionary\n")


def calculate_gpa(student_dictionary, grade_dictionary):
    """
    Calculates the GPA of a student by combining the grades of all their completed classes
    """
    while True:
        id = verify_id_input("What is the student's ID number? ")
        try:
            verification = input(f"Is this {student_dictionary[id]["name"]} the correct student? (Y/N) ").strip().lower()
            if verification == "y" or "yes":
                print("Verification Accepted")
                break
            elif verification == "n" or "no":
                print("Re-input the studen't ID")
            else:
                print("Type in y/yes or n/no")
        except KeyError:
            print("Dictionary or key does not exist")
    count = 0
    overall_sum = 0
    for grades in student_dictionary[id]["grades"].values():
        count += 1
        overall_sum += grade_dictionary[grades]
    gpa = overall_sum / count
    return gpa


def generate_report_students(dictionary):
    for student in dictionary:
        print(f"{dictionary[student]["name"]}\n")


def generate_report_maj(dictionary):
    major = verify_name_input("What major do you want to scan? ")
    for student in dictionary:
        if dictionary[student]["major"] == major:
            print(f"{dictionary[student]["name"]}\n")


def generate_report_gpa(student_dictionary, grade_dictionary):
    level_gpa = int(verify_id_input("What GPA do you want to be above? "))
    for student in student_dictionary:
        count = 0
        overall_sum = 0
        for grades in student_dictionary[student]["grades"].values():
            count += 1
            overall_sum += grade_dictionary[grades]
        gpa = overall_sum / count
        if gpa >= level_gpa:
            print(f"{student_dictionary[student]["name"]}")


def generate_individual_report(dictionary):
    while True:
        id = verify_id_input("Type in the student's id ")
        try:
            verification = input(f"Is this {student_data[id]["name"]} the correct student? (Y/N) ").strip().lower()
            if verification == "y" or "yes":
                print("Verification Accepted")
                break
            elif verification == "n" or "no":
                print("Re-input the studen't ID")
            else:
                print("Type in y/yes or n/no")
        except KeyError:
            print("Dictionary or key does not exist")
        print("\n====Student Report====")
        print(f"Name: {student_data[id]["name"]}")
        print(f"Major: {student_data[id]["major"]}")
        print(f"Courses:\n {student_data[id]["grades"]}\n")


if __name__ == "__main__":
    student_data = load_json_data("student_data.json")
    while True:  # This While loop ensures the program continues until it is forced close or the exit stage is complete.
        try:
            needed_response = input("\nType in what you want to do (Type the numbers)...\n"  # Each response here has a different if/elif catch down below
                                "Exit program with option 5 to save data if you are done...\n"
                                "1: Add new student\n"
                                "2: Add new/update grade\n"
                                "3: Calculate GPA\n"
                                "4: Generate Student Report\n"
                                "5: Exit the program\n\n")
            response = response_data[needed_response]
            if response == "generate":
                needed_response = input("\nWhat type of report do you want? \n"
                                "6: All Students\n"
                                "7: Students By Major\n"
                                "8: By GPA\n"
                                "9: For a Student\n")
                response = response_data[needed_response]
                if response == "all":
                    print("\nList of all students=========")
                    generate_report_students(student_data)
                elif response == "maj":
                    print("\nList of all students by major=========")
                    generate_report_maj(student_data)
                elif response == "allgpa":
                    print("\nList of all students by GPA=========")
                    generate_report_gpa(student_data, grade_data)
                elif response == "single":
                    print("\n====Student Report====")
                    generate_individual_report(student_data)
        except KeyError:
            print("Your response must be the number of the selection you want")
            response = 0
        if response == "add":
            add_student_record(student_data)
        elif response == "update":
            update_student_grades(student_data)
        elif response == "gpa":
            print(f"Student's GPA: {calculate_gpa(student_data, grade_data)}")
        elif response == "exit":
            dump_json_data(student_data, "student_data.json")
            break