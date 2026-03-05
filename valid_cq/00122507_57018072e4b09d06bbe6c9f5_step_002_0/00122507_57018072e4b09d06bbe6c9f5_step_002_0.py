import cadquery as cq

# Parametric dimensions
length = 100.0        # Distance between hole centers
boss_diam = 30.0      # Diameter of the rounded ends
hole_diam = 14.0      # Diameter of the through holes
arm_width = 18.0      # Width of the connecting arm
thickness = 10.0      # Thickness of the part
fillet_radius = 12.0  # Radius of the fillet connecting arm to bosses

# 1. Create the end bosses
# Create two circles at the specified distance and extrude them to form the eyes
bosses = (
    cq.Workplane("XY")
    .moveTo(-length / 2, 0).circle(boss_diam / 2)
    .moveTo(length / 2, 0).circle(boss_diam / 2)
    .extrude(thickness)
)

# 2. Create the connecting arm
# A rectangular solid connecting the two axes. 
# The length is set to the center distance, so it overlaps with the bosses up to their centers.
arm = (
    cq.Workplane("XY")
    .rect(length, arm_width)
    .extrude(thickness)
)

# 3. Combine parts and apply fillets
# Union the arm and bosses to create the basic shape.
joined_part = bosses.union(arm)

# Apply fillets to the vertical intersection edges to create the smooth, tapered neck.
# We filter edges to select only the vertical ones ('|Z') that are between the two centers.
filleted_part = (
    joined_part
    .edges("|Z")
    .filter(lambda e: abs(e.Center().x) < length / 2)
    .fillet(fillet_radius)
)

# 4. Cut the holes
# Select the top face and cut the mounting holes at the boss centers
result = (
    filleted_part
    .faces(">Z").workplane()
    .moveTo(-length / 2, 0).circle(hole_diam / 2)
    .moveTo(length / 2, 0).circle(hole_diam / 2)
    .cutThruAll()
)