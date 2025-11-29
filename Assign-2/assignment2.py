"""
# Name: Aduita Srivastava
# Date: [2025-11-22]
# Title: GradeBook Analyzer Mini-Project
# Course: Programming for Problem Solving using Python
"""

import csv
import statistics

#  Task 3: Statistical Functions 

def calculate_average(marks_dict):
    """Calculates the average of all marks."""
    marks = list(marks_dict.values())
    return statistics.mean(marks) if marks else 0

def calculate_median(marks_dict):
    """Calculates the median of all marks."""
    marks = list(marks_dict.values())
    return statistics.median(marks) if marks else 0

def find_max_score(marks_dict):
    """Finds the student and score for the highest mark."""
    if not marks_dict:
        return None, 0
    
# Find the student name (key) by the highest score (value)

    max_name = max(marks_dict, key=marks_dict.get)
    max_score = marks_dict[max_name]
    return max_name, max_score

def find_min_score(marks_dict):
    """Finds the student and score for the lowest mark."""
    if not marks_dict:
        return None, 0
    min_name = min(marks_dict, key=marks_dict.get)
    min_score = marks_dict[min_name]
    return min_name, min_score

#  Task 4: Grade Assignment Functions 

def assign_grade(score):
    """Helper function to assign a single letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def assign_all_grades(marks_dict):
    """Creates a new dictionary mapping students to their letter grades."""
    grades_dict = {}
    for name, mark in marks_dict.items():
        grades_dict[name] = assign_grade(mark)
    return grades_dict

def get_grade_distribution(grades_dict):
    """Counts the number of students who received each grade."""
    # Initialize a dictionary to count each grade
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in grades_dict.values():
        if grade in distribution:
            distribution[grade] += 1
    return distribution

#  Task 2: Data Input Functions 

def get_manual_data():
    """Task 2a: Gets student names and marks from manual user input."""
    print("\n--- Enter Manual Data ---")
    print("Type 'done' in the name field to finish.")
    marks_dict = {}
    while True:
        name = input("Enter student name: ").strip()
        if name.lower() == 'done':
            break
        
        if not name:
            print("Name cannot be empty.")
            continue
            
        try:
            # Get mark and convert it to an integer
            mark_input = input(f"Enter mark for {name}: ")
            mark = int(mark_input)
            
            if 0 <= mark <= 100: # Basic validation
                marks_dict[name] = mark
            else:
                print("Invalid mark. Please enter a number between 0 and 100.")
                
        except ValueError:
            print("Invalid mark. Please enter a whole number.")
            
    return marks_dict

def get_csv_data():
    """Task 2b: Loads student names and marks from a .csv file."""
    print("\n--- Load CSV Data ---")
    filename = input("Enter the CSV filename (e.g., marks.csv): ")
    marks_dict = {}
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            try:
                # Optional: Skip header row if your CSV has one
                # You can comment this out if your CSV has no header
                next(reader, None) 
            except StopIteration:
                pass # File is empty
            
            for row in reader:
                if row and len(row) >= 2: # Ensure row is not empty and has at least 2 columns
                    try:
                        name = row[0].strip()
                        mark_str = row[1].strip()
                        
                        if not name: # Skip if name is blank
                            print(f"Skipping row with blank name: {row}")
                            continue
                            
                        mark = int(mark_str)
                        
                        if 0 <= mark <= 100:
                            marks_dict[name] = mark
                        else:
                            print(f"Skipping {name}: mark {mark} is out of range (0-100).")
                            
                    except (ValueError, IndexError):
                        print(f"Skipping invalid data row: {row}")
                else:
                    # This will catch empty rows or rows with only one column
                    if row: 
                        print(f"Skipping malformed row (needs Name and Mark): {row}")
                    
        if not marks_dict:
            print(f"No valid data loaded from {filename}. File might be empty or in the wrong format.")
        else:
            print(f"Successfully loaded {len(marks_dict)} students from {filename}\n")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return marks_dict

#  Task 6: Display Functions 

def print_results_table(marks_dict, grades_dict):
    """(Task 6) Prints the final formatted results table."""
    print("\n" + "="*35)
    print("      --- Final Grade Report ---")
    print("=" * 35)
    # Print table header. f-string formatting:
    # <15 means left-aligned with 15 spaces
    # >5 means right-aligned with 5 spaces
    print(f"{'Name':<15} {'Mark':>7}   {'Grade':>5}")
    print("-" * 35)
    
    # Sort by name for consistent output
    for name in sorted(marks_dict.keys()):
        mark = marks_dict[name]
        grade = grades_dict.get(name, "N/A")
        print(f"{name:<15} {mark:>7}   {grade:>5}")
    print("-" * 35)

def print_statistics(marks_dict):
    """(Task 3) Prints all the calculated statistics."""
    print("\n--- Class Statistics ---")
    try:
        avg = calculate_average(marks_dict)
        print(f"Average Mark: {avg:.2f}") # Format to 2 decimal places
        
        median = calculate_median(marks_dict)
        print(f"Median Mark:  {median}")
        
        max_name, max_score = find_max_score(marks_dict)
        print(f"Highest Mark: {max_score} (by {max_name})")
        
        min_name, min_score = find_min_score(marks_dict)
        print(f"Lowest Mark:  {min_score} (by {min_name})")
    except statistics.StatisticsError:
        print("Not enough data to calculate statistics.")
    print("-" * 26)

def print_grade_distribution(distribution):
    """(Task 4) Prints the grade counts."""
    print("\n--- Grade Distribution ---")
    for grade, count in distribution.items():
        print(f"Grade {grade}: {count} student(s)")
    print("-" * 28)

def print_pass_fail(marks_dict):
    """(Task 5) Prints the pass/fail lists using list comprehensions."""
    print("\n--- Pass/Fail Lists (Passing >= 40) ---")
    
    #  Task 5: List Comprehensions 
    # We filter the dictionary's .items() which gives (name, mark)
    # Sorting the names alphabetically
    passed_students = sorted([name for name, mark in marks_dict.items() if mark >= 40])
    failed_students = sorted([name for name, mark in marks_dict.items() if mark < 40])
    
    print(f"Total Passed: {len(passed_students)}")
    print("Students who passed:", ", ".join(passed_students) or "None")
    
    print(f"\nTotal Failed: {len(failed_students)}")
    print("Students who failed:", ", ".join(failed_students) or "None")
    print("-" * 40)

#  Task 1 & 6: Main Application Loop 

def main():
    """Main function to run the gradebook analyzer."""
    
    marks_data = {} # This will store our data {"Student": Mark}
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Enter marks manually")
        print("2. Load marks from CSV")
        print("3. Exit")
        choice = input("Please choose an option (1-3): ")

        if choice == '1':
            marks_data = get_manual_data()
            break # Exit menu loop and proceed to analysis
        elif choice == '2':
            marks_data = get_csv_data()
            break # Exit menu loop and proceed to analysis
        elif choice == '3':
            print("Goodbye!")
            return False # Signal to the outer loop to exit
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # If no data was loaded (e.g., file not found or user quit manual entry)
    if not marks_data:
        print("No data loaded. Returning to main menu.")
        return True # Signal to the outer loop to continue

    #  Run All Analysis Tasks 
    
    print(f"\nAnalysis starting for {len(marks_data)} student(s)...")
    
    # Task 3: Calculate and print statistics
    print_statistics(marks_data)
    
    # Task 4: Assign grades and print distribution
    grades_data = assign_all_grades(marks_data)
    distribution = get_grade_distribution(grades_data)
    print_grade_distribution(distribution)
    
    # Task 5: Print pass/fail lists
    print_pass_fail(marks_data)
    
    # Task 6: Print final results table
    print_results_table(marks_data, grades_data)
    
    print("\nAnalysis complete.")
    return True # Signal to the outer loop to continue

#  This is the entry point of the script 
if __name__ == "__main__":
    
    # --- Task 1: Welcome Message ---
    print("=" * 40)
    print("  Welcome to the GradeBook Analyzer CLI")
    print("=" * 40)
    
    #  Task 6: User Loop 
    while True: # Loop to allow for repeated analysis
        keep_running = main() # Run the main program
        
        if not keep_running:
            break # Exit if main() returned False (user chose 'Exit')
        
        # Ask to run again
        print("\n" + "=" * 40)
        again = input("Do you want to run a new analysis? (yes/no): ")
        if again.lower().strip() not in ['yes', 'y']:
            print("Goodbye!")
            break
        print("\n" + "=" * 40) # Add separator for the new run