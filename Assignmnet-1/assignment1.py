
# Project Title : Daily Calorie Tracker
# Author        : Aduita Srivastava
import datetime

#  Welcome Message 
print("\n===============================")
print("    Welcome to Calorie Tracker CLI Tool!   ")
print("===============================\n")
print("This tool helps you log your meals, track total calories, compare them with your daily limit /nand provides a summary report.\n")

#  Input & Data Collection 
meals = []       # List to store meal names
calories = []    # List to store calorie values

num_meals = int(input("How many meals would you like to log today? "))

for i in range(num_meals):
    meal_name = input(f"\nEnter meal {i+1} name: ")
    calorie_value = float(input(f"Enter calories for {meal_name}: "))
    meals.append(meal_name)
    calories.append(calorie_value)

#  Calorie Calculations 
total_calories = sum(calories)
average_calories = total_calories / len(calories)
daily_limit = float(input("\n Enter your daily calorie limit: "))

#  Exceed Limit Warning System
if total_calories > daily_limit:
    status_message = " You have exceeded your daily calorie limit!"
else:
    status_message = " You are within your daily calorie limit. Good job!"

#  Output 
print("\n\n===== DAILY CALORIE REPORT =====")
print("Meal Name\tCalories")
print("--------------------------------")

for meal, cal in zip(meals, calories):
    print(f"{meal:<12}\t{cal:.2f}")

print("--------------------------------")
print(f"Total:\t\t{total_calories:.2f}")
print(f"Average:\t{average_calories:.2f}")
print("--------------------------------")
print(status_message)

#  Save Session Log to File
save_choice = input("\nWould you like to save this session to a file? (yes/no): ").strip().lower()

if save_choice == "yes":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"calorie_log_{timestamp}.txt"
    
    with open(filename, "w") as file:
        file.write("===== DAILY CALORIE REPORT =====\n")
        file.write(f"Session Date/Time: {timestamp}\n\n")
        file.write("Meal Name\tCalories\n")
        file.write("--------------------------------\n")
        for meal, cal in zip(meals, calories):
            file.write(f"{meal:<12}\t{cal:.2f}\n")
        file.write("--------------------------------\n")
        file.write(f"Total:\t\t{total_calories:.2f}\n")
        file.write(f"Average:\t{average_calories:.2f}\n")
        file.write("--------------------------------\n")
        file.write(f"Status: {status_message}\n")
    
    print(f"\n Session saved successfully as '{filename}'.")
else:
    print("\nSession not saved. Goodbye! ")

print("\nThank you for using the Calorie Tracker!")
