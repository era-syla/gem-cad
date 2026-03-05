import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
outer_diameter = 50.0
height = 50.0

# Stepped hole parameters
# List of (diameter, depth_from_top) tuples
# The depths are cumulative from the top face
steps = [
    (40.0, 5.0),   # First step: diameter 40, depth 5
    (35.0, 10.0),  # Second step: diameter 35, depth 10
    (30.0, 15.0),  # Third step: diameter 30, depth 15
    (25.0, 20.0),  # Fourth step: diameter 25, depth 20
    (20.0, 25.0),  # Fifth step: diameter 20, depth 25
    (15.0, 30.0),  # Sixth step: diameter 15, depth 30
]
# Final thru-hole or deepest blind hole
bottom_hole_diameter = 10.0
bottom_hole_depth = height # Making it a through-hole for this interpretation, or just deep

# --- Modeling ---

# 1. Create the base cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# 2. Cut the steps
# We work from the top face downwards
for step_dia, step_depth in steps:
    # Select the top face
    result = (
        result.faces(">Z")
        .workplane()
        .circle(step_dia / 2.0)
        .cutBlind(-step_depth)
    )

# 3. Create the final bottom hole
# This goes all the way through or to the remaining depth
result = (
    result.faces(">Z")
    .workplane()
    .circle(bottom_hole_diameter / 2.0)
    .cutBlind(-height) # Cut all the way through
)

# Alternatively, if the image implies a specific non-through bottom, 
# one could adjust the last cut depth. Based on the visual of a "stepped cone", 
# a through hole or very deep hole is a safe geometric assumption.