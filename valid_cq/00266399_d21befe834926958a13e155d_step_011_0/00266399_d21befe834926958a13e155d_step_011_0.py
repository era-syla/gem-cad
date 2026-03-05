import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0         # Total length of the part
height = 20.0          # Height of the side walls
width = 15.0           # Total outer width
wall_thickness = 2.5   # Thickness of the side walls
base_thickness = 2.5   # Thickness of the bottom connecting plate
rim_size = 3.5         # Width of the material surrounding the slot

# Derived dimensions for the inner slot to maintain uniform rim
slot_length = length - (2 * rim_size)
slot_height = height - (2 * rim_size)
# The length of the straight section of the stadium shape (Length - 2*Radius)
# Radius is height/2.
straight_length = length - height

# --- Modeling ---

# 1. Define the 2D profile for the side walls
# We use a Sketch with a 'slot' (stadium) shape and subtract a smaller slot.
wall_sketch = (
    cq.Sketch()
    .slot(length, height, angle=0.0)            # Outer wall shape
    .slot(slot_length, slot_height, angle=0.0, mode='s') # Inner slot cutout
)

# 2. Create the first side wall
# Extrude the sketch perpendicular to the XZ plane (along Y)
wall_front = (
    cq.Workplane("XZ")
    .placeSketch(wall_sketch)
    .extrude(wall_thickness)
    .translate((0, width/2 - wall_thickness, 0)) # Position at the front face
)

# 3. Create the second side wall
# Create the same extrusion and position it at the back face
wall_back = (
    cq.Workplane("XZ")
    .placeSketch(wall_sketch)
    .extrude(wall_thickness)
    .translate((0, -width/2, 0)) # Position at the back face
)

# 4. Create the Base
# The base connects the two walls at the bottom.
# It spans the straight section of the part length.
base = (
    cq.Workplane("XY")
    .rect(straight_length, width) # Rectangular base connecting the straight sections
    .extrude(base_thickness)
    .translate((0, 0, -height/2)) # Align flush with the bottom of the walls
)

# 5. Combine parts into a single solid
result = wall_front.union(wall_back).union(base)