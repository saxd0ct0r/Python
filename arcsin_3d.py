import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cmath

# Define the range for x (real input)
x1 = np.linspace(-3, -1, 500)  # x < -1
x2 = np.linspace(-1, 1, 500)   # x in [-1, 1]
x3 = np.linspace(1, 3, 500)    # x > 1

# Compute arcsine for principal branch
arcsine1 = [cmath.asin(x_val) for x_val in x1]
arcsine2 = [cmath.asin(x_val) for x_val in x2]
arcsine3 = [cmath.asin(x_val) for x_val in x3]

# Extract real and imaginary parts
real_part1 = [z.real for z in arcsine1]
imag_part1 = [z.imag for z in arcsine1]
real_part2 = [z.real for z in arcsine2]
imag_part2 = [z.imag for z in arcsine2]
real_part3 = [z.real for z in arcsine3]
imag_part3 = [z.imag for z in arcsine3]

# Create the 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot segments with different colors
ax.plot(x1, real_part1, imag_part1, color='blue', label='x < -1 (Positive Imag)')
ax.plot(x2, real_part2, imag_part2, color='red', label='x in [-1, 1] (Real)')
ax.plot(x3, real_part3, imag_part3, color='green', label='x > 1 (Negative Imag)')

# Add annotations to highlight negative imaginary part
ax.text(1.5, np.pi, -1, 'Negative Imaginary\nfor x > 1', color='green', fontsize=10)

ax.set_xlabel('Input x (Real)')
ax.set_ylabel('Real part of arcsin(x)')
ax.set_zlabel('Imaginary part of arcsin(x)')
ax.set_title('3D Plot of Principal Branch of Arcsine Function')
ax.grid(True)
ax.legend()
# Set axis limits
ax.set_xlim([-3, 3])
ax.set_ylim([-np.pi, np.pi])
ax.set_zlim([-3, 3])
plt.show()