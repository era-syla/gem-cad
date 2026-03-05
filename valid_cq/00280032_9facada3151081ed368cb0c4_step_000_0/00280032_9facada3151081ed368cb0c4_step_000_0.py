import cadquery as cq

# --- Geometric Parameters ---
length = 300.0
height = 30.0
width = 20.0       # Width of the top horizontal flange
thickness = 5.0    # Thickness of the material
notch_size = 5.0   # Size of the cutout at the start

# --- 1. Create Base L-Profile ---
# Sketch on YZ plane (Side view) and extrude along X (Length)
# Origin (0,0,0) is at the bottom-front-left corner.
# The vertical leg is at Y=0, horizontal leg is at Z=height.
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (0, height),
        (width, height),
        (width, height - thickness),
        (thickness, height - thickness),
        (thickness, 0),
        (0, 0)
    ])
    .close()
    .extrude(length)
)

# --- 2. Top Face Features (Slots & Holes) ---
# Work on the top face (Z = height). 
# We use ProjectedOrigin to maintain global X coordinates.
# Features are centered along the flange width (Y axis on the face).

y_center = width / 2.0

# Define dimensions and positions
slot1_length = 140.0
slot1_width = 8.0
slot1_x = 20.0 + slot1_length / 2.0  # Center position

hole1_dia = 8.0
hole1_x = 185.0

slot2_length = 40.0
slot2_width = 8.0
slot2_x = 210.0 + slot2_length / 2.0 # Center position

hole2_dia = 8.0
hole2_x = 275.0

result = (
    result
    .faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    
    # Long Slot
    .moveTo(slot1_x, y_center)
    .slot2D(slot1_length, slot1_width)
    .cutThruAll()
    
    # First Circular Hole
    .moveTo(hole1_x, y_center)
    .circle(hole1_dia / 2.0)
    .cutThruAll()
    
    # Short Slot / Oblong
    .moveTo(slot2_x, y_center)
    .slot2D(slot2_length, slot2_width)
    .cutThruAll()
    
    # Second Circular Hole
    .moveTo(hole2_x, y_center)
    .circle(hole2_dia / 2.0)
    .cutThruAll()
)

# --- 3. Front Face Features (Mounting Holes) ---
# Work on the front vertical face (Y = 0).
# Holes are typically countersunk for flush screws.

front_hole_y = height / 2.0
front_hole_dia = 5.0
csk_dia = 9.0
csk_angle = 82
front_holes_x = [15.0, 165.0, 285.0]

result = (
    result
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints([(x, front_hole_y) for x in front_holes_x])
    .cskHole(front_hole_dia, csk_dia, csk_angle)
)

# --- 4. End Detail (Notch) ---
# Cut a small rectangular notch at the bottom-left corner (x=0, z=0).
# We create a cutting tool and subtract it.

result = result.cut(
    cq.Workplane("XY")
    .rect(notch_size * 2, width * 3) # Create a large enough rectangle
    .extrude(notch_size)             # Height of the notch
    .translate((notch_size, 0, 0))   # Shift so the cut starts at X=0
)