import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cmath

# Define the range for x (real input)
x = np.linspace(-2, 2, 1000)

# Compute arcsine for real x
arcsine = [cmath.asin(x_val) for x_val in x]

# Extract real and imaginary parts
real_part = [z.real for z in arcsine]
imag_part = [z.imag for z in arcsine]

# Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, real_part, imag_part, color='blue', label='arcsin(x)')
ax.set_xlabel('Input x (Real)')
ax.set_ylabel('Real part of arcsin(x)')
ax.set_zlabel('Imaginary part of arcsin(x)')
ax.set_title('3D Plot of Arcsine Function (Real and Imaginary Parts)')
ax.grid(True)
ax.legend()
# Set axis limits for better visualization
ax.set_xlim([-2, 2])
ax.set_ylim([-np.pi/2, np.pi/2])
ax.set_zlim([-2, 2])
plt.show()