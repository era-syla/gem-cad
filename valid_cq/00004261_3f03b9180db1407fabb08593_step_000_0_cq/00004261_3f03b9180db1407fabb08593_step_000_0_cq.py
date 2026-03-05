import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_diameter = 100.0  # Estimated diameter of the main disk
plate_thickness = 5.0   # Estimated thickness of the plate

# Central bore dimensions
center_hole_diameter = 25.0  # Large central hole

# Inner hole pattern
inner_bc_diameter = 40.0     # Bolt circle diameter for inner holes
inner_hole_diameter = 3.5    # Diameter of inner small holes
num_inner_holes = 4          # Number of holes in the inner ring

# Outer hole pattern
outer_bc_diameter = 80.0     # Bolt circle diameter for outer holes
outer_hole_diameter = 3.5    # Diameter of outer holes
num_outer_holes = 6          # Number of holes in the outer ring

# --- Geometry Construction ---

# 1. Create the base disk
result = cq.Workplane("XY").circle(plate_diameter / 2).extrude(plate_thickness)

# 2. Cut the central hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# 3. Create the inner ring of holes
# We use polar coordinates to position the holes
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(inner_bc_diameter / 2, 0, 360, num_inner_holes)
    .hole(inner_hole_diameter)
)

# 4. Create the outer ring of holes
# Note: In the image, the outer holes seem offset or aligned differently.
# A standard polar array distributes them evenly.
# Assuming standard even distribution starting at angle 0.
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(outer_bc_diameter / 2, 30, 360, num_outer_holes) # Starting at 30 deg to stagger visually
    .hole(outer_hole_diameter)
)

# Return the final result
# The variable 'result' contains the final geometry