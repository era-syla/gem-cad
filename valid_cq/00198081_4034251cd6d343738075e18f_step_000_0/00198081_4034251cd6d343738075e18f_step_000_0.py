import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_length = 120.0
base_width = 20.0
base_height = 6.0

# Leg dimensions
leg_spacing = 50.0      # Distance between leg centers
leg_width = 10.0        # Length along X axis
leg_thickness = 8.0     # Thickness along Y axis
leg_height = 12.0       # Height from base to bird body

# Bird body dimensions
bird_thickness = 8.0
bird_elevation = (base_height / 2.0) + leg_height

# --- Geometry Construction ---

# 1. Create the Base Bar
# A simple rectangular box centered at the origin
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Create the Vertical Supports (Legs)
# Positioned on top of the base
legs = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2.0)
    .pushPoints([(-leg_spacing / 2.0, 0), (leg_spacing / 2.0, 0)])
    .rect(leg_width, leg_thickness)
    .extrude(leg_height)
)

# 3. Create the Bird Silhouette
# We define the profile on the XZ plane to stand it upright.
# The plane is offset in Y to center the extrusion thickness.
bird_plane = (
    cq.Workplane("XZ")
    .workplane(offset=-bird_thickness / 2.0)
    .center(0, bird_elevation)
)

# Points defining the organic shape of the bird (duck style)
# Coordinates relative to the center point between the legs at the bottom of the bird
spline_points = [
    (-45.0, 5.0),    # Throat curve
    (-60.0, 15.0),   # Beak tip
    (-48.0, 25.0),   # Forehead
    (-35.0, 28.0),   # Head top
    (-20.0, 20.0),   # Neck dip
    (15.0, 45.0),    # Back hump high point
    (65.0, 30.0),    # Tail tip
    (50.0, 15.0),    # Under tail
    (30.0, 0.0)      # End of bottom curve
]

bird_body = (
    bird_plane
    .moveTo(30.0, 0.0)       # Start at bottom right (near rear leg)
    .lineTo(-30.0, 0.0)      # Flat bottom line between legs
    .spline(spline_points, includeCurrent=True) # Organic curve for the rest
    .close()
    .extrude(bird_thickness)
)

# 4. Create the Eye Hole
eye_hole = (
    cq.Workplane("XZ")
    .workplane(offset=-bird_thickness) # Start from outside to ensure clean cut
    .center(0, bird_elevation)
    .moveTo(-42.0, 20.0)     # Approximate eye position
    .circle(2.5)
    .extrude(bird_thickness * 3)
)

# --- Final Assembly ---
# Combine base, legs, and bird, then cut the eye hole
result = base.union(legs).union(bird_body).cut(eye_hole)