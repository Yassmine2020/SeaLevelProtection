import numpy as np
import matplotlib.pyplot as plt

# Create the array
arr = np.array([[8, 8, 7, 7, 6, 6, 7, 6, 2],
                [2, 4, 7, 6, 8, 5, 1, 5, 2],
                [4, 8, 7, 3, 4, 5, 2, 5, 6],
                [6, 8, 2, 6, 5, 2, 8, 8, 7],
                [1, 8, 8, 3, 4, 9, 2, 3, 6],
                [9, 5, 7, 7, 3, 1, 1, 3, 2],
                [5, 3, 2, 5, 3, 4, 2, 1, 1],
                [7, 3, 9, 6, 9, 6, 2, 4, 2],
                [7, 4, 3, 1, 1, 1, 5, 1, 8]])

# Plot the heatmap
plt.imshow(arr, cmap='hot')

# Add the colorbar legend
plt.colorbar()

# Show the plot
plt.show()
