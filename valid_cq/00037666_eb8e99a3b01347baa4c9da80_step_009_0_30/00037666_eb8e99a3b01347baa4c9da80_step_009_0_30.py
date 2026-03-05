import cadquery as cq

# Parameters for the mechanical link
num_holes = 5                # Number of holes in the bar
pitch = 20.0                 # Distance between hole centers (mm)
bar_width = 20.0             # Width of the bar (mm)
thickness = 3.0              # Thickness of the material (mm)
hole_diameter = 10.0         # Diameter of the holes (mm)

# Calculations
# Calculate the total length of the slot shape (tip-to-tip)
# Center-to-center distance + one width (radius * 2)
center_distance = (num_holes - 1) * pitch
total_length = center_distance + bar_width

# Generate hole coordinates centered around the origin
hole_points = [
    (i * pitch - center_distance / 2.0, 0) 
    for i in range(num_holes)
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Create the outer stadium/slot profile
    # slot2D defines the shape by total length and width (diameter of the rounded ends)
    .slot2D(length=total_length, diameter=bar_width)
    # Create the hole profiles
    .pushPoints(hole_points)
    .circle(hole_diameter / 2.0)
    # Extrude combined profiles (inner profiles become voids)
    .extrude(thickness)
)