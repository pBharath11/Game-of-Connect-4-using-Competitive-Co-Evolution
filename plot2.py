import matplotlib.pyplot as plt

# Data
no_of_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
win_count = [0, 1, 1, 2, 3, 4, 5, 5, 6, 7]

# Create a line chart
plt.figure(figsize=(10, 6))
plt.plot(no_of_games, win_count, marker='o', linestyle='-')

# Adding labels and title
plt.xlabel("No of games played")
plt.ylabel("No of AI wins")
plt.title("games played vs. No of AI wins")

# Show the plot
plt.grid(True)
plt.show()