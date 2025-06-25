import random

'''
1 for snake
-1 for water 
0 for gun 
'''

youDict = {"s": 1, "w": -1, "g": 0}
reverseDict = {1: "snake", -1: "water", 0: "gun"}

# Get user input
youstr = input("Enter your choice (s for snake, w for water, g for gun): ").lower()

# Check for valid input
if youstr not in youDict:
    print("Invalid input! Please choose 's', 'w', or 'g'.")
else:
    computer = random.choice([-1, 0, 1])
    you = youDict[youstr]

    print(f"You chose {reverseDict[you]}")
    print(f"Computer chose {reverseDict[computer]}")

    if computer == you:
        print("It's a draw!")
    elif (you == 1 and computer == -1) or (you == -1 and computer == 0) or (you == 0 and computer == 1):
        print("You win!")
    else:
        print("You lose!")
