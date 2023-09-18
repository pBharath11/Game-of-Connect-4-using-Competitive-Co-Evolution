import matplotlib.pyplot as plt

# Data
gen_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
win_count = [15, 14, 10, 6, 13, 15, 15, 7, 4, 14, 15, 15]

# Create a line chart
plt.figure(figsize=(10, 6))
plt.plot(gen_count, win_count, marker='o', linestyle='-')

# Adding labels and title
plt.xlabel("No of AI generations ran")
plt.ylabel("Win Count during each evolution")
plt.title("AI generations ran vs. Win Count during each evolution")

# Show the plot
plt.grid(True)
plt.show()