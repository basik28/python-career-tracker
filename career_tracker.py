
def calculate_weekly_hours(daily_hours):
    return daily_hours * 6


def evaluate_progress(weekly_hours):
    if weekly_hours >= 18:
        return "Excellent! Keep going."
    elif weekly_hours >= 12:
        return "Good! You are making progress."
    else:
        return "You need to study more."


print("==========================")
print("     AI CAREER TRACKER")
print("==========================")

name = input("Your name: ")
daily_hours = float(input("Daily study hours: "))
python_level = input("Your Python level: ")

weekly_hours = calculate_weekly_hours(daily_hours)

progress = evaluate_progress(weekly_hours)

print("\n----- YOUR REPORT -----")
print("Name:", name)
print("Python Level:", python_level)
print("Daily Hours:", daily_hours)
print("Weekly Hours:", weekly_hours)
print("Progress:", progress)

print("\nYour study schedule:")

for day in range(1, 7):
    print("Day", day, "- Python Training")
