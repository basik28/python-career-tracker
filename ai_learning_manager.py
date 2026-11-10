
user = {
    "name": "Baris",
    "goal": "AI Engineer",
    "daily_hours": 3
}

topics = [
    "Python",
    "API",
    "Artificial Intelligence",
    "AI Automation",
    "Machine Learning"
]

print("==========================")
print("     AI LEARNING MANAGER")
print("==========================")

print("Student:", user["name"])
print("Career Goal:", user["goal"])
print("Daily Study Hours:", user["daily_hours"])

print("\nYour Learning Topics:")

for index, topic in enumerate(topics, start=1):
    print(index, "-", topic)

print("\nTotal Topics:", len(topics))

completed = 0

while completed < len(topics):

    print("\nNext topic:", topics[completed])

    answer = input("Did you complete this topic? (yes/no): ")

    if answer.lower() == "yes":
        completed += 1
        print("Great! Progress saved.")

    elif answer.lower() == "no":
        print("Keep practicing!")

    else:
        print("Please enter yes or no.")

    if answer.lower() == "no":
        break

print("\nCompleted Topics:", completed)
print("Remaining Topics:", len(topics) - completed)