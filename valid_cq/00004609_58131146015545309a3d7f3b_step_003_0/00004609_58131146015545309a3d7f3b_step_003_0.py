import cadquery as cq

# Parametric dimensions for the model
head_diameter = 22.0     # Maximum diameter of the countersunk head
head_height = 7.0        # Length of the tapered head section
shank_diameter = 10.0    # Diameter of the cylindrical body
shank_length = 30.0      # Length of the straight cylindrical section
tip_height = 3.5         # Length of the tapered tip
tip_end_diameter = 6.0   # Diameter at the very end of the tip

# Calculate radii for the revolution profile
r_head = head_diameter / 2.0
r_shank = shank_diameter / 2.0
r_tip = tip_end_diameter / 2.0

# Define the points for the 2D profile to be revolved.
# The profile is defined in the XZ plane, where X corresponds to radius and Z to length.
# (0,0) is located at the center of the large flat face of the head.
points = [
    (0, 0),                                           # Center of the head face
    (r_head, 0),                                      # Outer edge of the head face
    (r_shank, head_height),                           # Transition from head to shank
    (r_shank, head_height + shank_length),            # End of the straight shank
    (r_tip, head_height + shank_length + tip_height), # End of the tip taper
    (0, head_height + shank_length + tip_height)      # Center of the tip end
]

# Create the solid by revolving the profile 360 degrees
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)