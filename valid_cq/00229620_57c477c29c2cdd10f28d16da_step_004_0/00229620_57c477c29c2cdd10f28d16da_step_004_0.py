import cadquery as cq

# Define parametric dimensions
total_length = 65.0
body_width = 8.0
front_height = 9.0
mid_height = 13.0
tail_height_start = 9.5
tail_height_end = 4.0

# 1. Create the Main Body Profile (Side View)
# Defined on the XZ plane starting from the bottom-front
profile_points = [
    (0, 2.0),      # Front nose bottom
    (0, 9.0),      # Front nose top
    (8, 9.0),      # Step back
    (8, 13.0),     # Step up to main block
    (36, 13.0),    # Main block top end
    (36, 9.5),     # Step down
    (50, 9.5),     # Rear flat section
    (65, 4.0),     # Tail tip top
    (65, 2.0),     # Tail tip bottom
    (45, 2.0),     # Tail underside slope start
    (12, 2.0),     # Bottom flat run
    (12, 0.0),     # Bottom hook notch back
    (5, 0.0),      # Bottom hook
    (5, 2.0),      # Bottom hook notch front
    (0, 2.0)       # Close loop
]

# Extrude the base shape symmetrically along Y
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(body_width / 2.0, both=True)
)

# 2. Create the Front Slot
# Cut a rectangular pocket into the front face
result = (
    result.faces("<X")
    .workplane()
    .center(0, 1.5)  # Adjust vertical center relative to face
    .rect(4.0, 5.0)  # Slot dimensions
    .cutBlind(-7.0)  # Depth of the slot
)

# 3. Create the Side Relief (Zig-Zag Recess)
# Sketch on the side face (>Y) to create the aesthetic/structural recess
recess_points = [
    (14, 3.5),   # Bottom-left of recess
    (40, 3.5),   # Bottom-right
    (48, 6.0),   # Angled up towards tail
    (48, 8.5),   # Vertical up
    (36, 8.5),   # Step back
    (36, 11.0),  # Vertical up to top block area
    (14, 7.5)    # Angled down to front
]

result = (
    result.faces(">Y")
    .workplane(centerOption="ProjectedOrigin")
    .polyline(recess_points)
    .close()
    .cutBlind(-1.0)  # Shallow cut depth
)

# 4. Add the Rear Top Plate Detail
# A slightly wider flat platform at the rear transition
rear_plate = (
    cq.Workplane("XY")
    .workplane(offset=9.5)  # Z-height of the rear section
    .center(49, 0)          # X-position
    .rect(12, 10)           # Width 12 (wider than body), Length 10
    .extrude(1.5)           # Thickness of the plate
)

result = result.union(rear_plate)

# 5. Final Details
# Chamfer the top edge of the front nose
result = result.edges(
    cq.selectors.BoxSelector((0, -4, 8.9), (8, 4, 9.1))
).chamfer(1.0)