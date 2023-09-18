import matplotlib.pyplot as plt

# Data
Move_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
win_count = [5, 4, 0, 0, 0, 5, 3, 0, 0, 0, 4, 5, 5]

# Create a line chart
plt.figure(figsize=(10, 6))
plt.plot(Move_count, win_count, marker='o', linestyle='-')

# Adding labels and title
plt.xlabel("No of AI moves")
plt.ylabel("Win Count during each evolution")
plt.title("No of AI moves vs. Win Count during each evolution")

# Show the plot
plt.grid(True)
plt.show()