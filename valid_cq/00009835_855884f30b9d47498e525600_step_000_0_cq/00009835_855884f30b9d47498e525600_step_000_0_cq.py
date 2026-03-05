import cadquery as cq

# Parameters
base_width = 40.0
base_length = 40.0
base_thickness = 3.0
base_fillet_radius = 5.0

boss_diameter = 20.0
boss_height = 15.0  # Height from the top of the base
hole_diameter = 8.0

rib_thickness = 3.0
rib_height = 10.0  # Height of the rib against the boss
rib_width = 8.0    # Length of the rib along the base

# 1. Create the Base Plate
# Create a rectangle and extrude it
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .edges("|Z")
    .fillet(base_fillet_radius)
)

# 2. Create the Central Boss
# Create a cylinder on top of the base
boss = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness / 2) # Start from top of base (box is centered on Z=0, so top is thickness/2)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 3. Create the Ribs
# We need 4 ribs spaced 90 degrees apart.
# We will create one rib profile and revolve/duplicate it, or sketch and extrude.
# A simple way is to sketch a triangle on a vertical plane and extrude it symmetrically.

# Define the rib profile (a right-angled triangle)
# Coordinates relative to the center of the rib sketch
# We will sketch on the XZ plane for the ribs aligned with X
rib_profile_pts = [
    (boss_diameter / 2, 0),  # Start at base of boss
    (boss_diameter / 2 + rib_width, 0),  # Go out along base
    (boss_diameter / 2, rib_height)  # Go up the boss
]

# Create one set of ribs along the X axis
rib_x = (
    cq.Workplane("XZ")
    .workplane(offset=-rib_thickness / 2)  # Center the rib thickness
    .workplane(origin=(0, base_thickness/2, 0)) # Move origin to top surface of base
    .polyline(rib_profile_pts)
    .close()
    .extrude(rib_thickness)
)

# Create the second set of ribs along the X axis (rotated 180 or mirrored) - actually simpler to just rotate copies
ribs_rotated = rib_x.rotate((0, 0, 0), (0, 0, 1), 90)
ribs_rotated_2 = rib_x.rotate((0, 0, 0), (0, 0, 1), 180)
ribs_rotated_3 = rib_x.rotate((0, 0, 0), (0, 0, 1), 270)

# Combine everything
combined_solid = base.union(boss).union(rib_x).union(ribs_rotated).union(ribs_rotated_2).union(ribs_rotated_3)

# 4. Create the Center Hole
# Cut the hole through the entire assembly
result = (
    combined_solid
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# If running in an environment that supports show_object (like CQ-editor)
# show_object(result)