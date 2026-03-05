import cadquery as cq

# --- Dimensions and Parameters ---
total_length = 180.0
max_height = 32.0
thickness = 2.5
hole_diameter = 6.0

# Key Coordinates for the profile
# Tip is at (0,0)
tip_pt = (0.0, 0.0)
peak_pt = (70.0, 32.0)            # Highest point of the top curve
tail_start_top = (150.0, 18.0)    # Where the curve ends and steps down
tail_start_step = (150.0, 10.0)   # The bottom of the step
tail_flat_end = (175.0, 10.0)     # End of the flat tail section
tail_tip_pt = (180.0, 5.0)        # The pointy tip of the tail
tail_bottom_return = (175.0, 0.0) # Where the tail returns to the baseline

# Notch locations (start and end X coordinates)
# Notches are cut into the bottom edge
notch_depth = 4.0
notch1_x = (85.0, 100.0)
notch2_x = (115.0, 130.0)

# Hole locations
hole1_pos = (20.0, 9.0)
hole2_pos = (140.0, 13.0)

# --- Geometry Generation ---

# Create the main profile wire
# We trace the perimeter: Top Curve -> Tail -> Bottom Edge (with notches)
result = (
    cq.Workplane("XY")
    .moveTo(*tip_pt)
    # 1. Top curved edge (Airfoil shape)
    .spline([peak_pt, tail_start_top], includeCurrent=True)
    # 2. Tail section step-down
    .lineTo(*tail_start_step)
    .lineTo(*tail_flat_end)
    # 3. Tail tip chamfer
    .lineTo(*tail_tip_pt)
    .lineTo(*tail_bottom_return)
    # 4. Bottom edge traversing right-to-left, adding notches
    .lineTo(notch2_x[1], 0.0)           # Line to start of notch 2
    .lineTo(notch2_x[1], notch_depth)   # Notch 2 Up
    .lineTo(notch2_x[0], notch_depth)   # Notch 2 Over
    .lineTo(notch2_x[0], 0.0)           # Notch 2 Down
    .lineTo(notch1_x[1], 0.0)           # Line to start of notch 1
    .lineTo(notch1_x[1], notch_depth)   # Notch 1 Up
    .lineTo(notch1_x[0], notch_depth)   # Notch 1 Over
    .lineTo(notch1_x[0], 0.0)           # Notch 1 Down
    .close()                            # Close back to tip (0,0)
    .extrude(thickness)
)

# Cut the mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([hole1_pos, hole2_pos])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)