import cadquery as cq

# Geometric Parameters
radius = 4.0          # Radius of the cylinder
length = 60.0         # Height of the cylindrical section
tip_height = 4.0      # Height of the conical tip

# Define the points for the profile to be revolved.
# The profile is defined in the XZ plane and consists of half the cross-section.
# Points: Bottom-Center -> Bottom-Right -> Top-Right (Start of cone) -> Top-Center (Tip)
profile_points = [
    (0, 0),
    (radius, 0),
    (radius, length),
    (0, length + tip_height)
]

# Create the solid by revolving the profile around the vertical axis (Z-axis by default for XZ plane)
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)