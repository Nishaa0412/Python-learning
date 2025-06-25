import datetime

# Ask the user for their name
name = input("Enter your name: ")

# Get the current hour
current_hour = datetime.datetime.now().hour

# Determine the greeting
if 5 <= current_hour < 12:
    greeting = "Good morning"
elif 12 <= current_hour < 17:
    greeting = "Good afternoon"
elif 17 <= current_hour < 21:
    greeting = "Good evening"
else:
    greeting = "Good night"

# Print the greeting with the user's name
print(f"{greeting}, {name}!")
