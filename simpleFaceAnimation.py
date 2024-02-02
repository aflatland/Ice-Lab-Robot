import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Setting up the figure
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal', 'box')
ax.axis('off')

# Drawing the static parts of the face: eyes
left_eye = plt.Circle((-0.5, 0.5), 0.1, color='black')
right_eye = plt.Circle((0.5, 0.5), 0.1, color='black')
ax.add_patch(left_eye)
ax.add_patch(right_eye)

# Initial mouth
mouth_width = 0.6
mouth_height = 0.1
mouth = plt.Rectangle((-mouth_width/2, -0.5), mouth_width, mouth_height, color='black', fill=True)
ax.add_patch(mouth)

# Function to update the mouth for each frame
def update(frame):
    mouth.set_height(0.1 * np.abs(np.sin(frame * np.pi / 10)))  # Sinusoidal movement for talking effect
    return [mouth]

# Creating the animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 20), interval=30, blit=True)

# Display the animation
plt.show()
