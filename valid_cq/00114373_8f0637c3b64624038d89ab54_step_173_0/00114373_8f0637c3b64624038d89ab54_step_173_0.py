import cadquery as cq

# --- Model Parameters ---
# Left Object Dimensions
l_plate_width = 35.0
l_plate_height = 100.0
l_plate_thick = 3.0
pin_diameter = 2.0
pin_length = 45.0
pin_margin_z = 10.0  # Distance from top/bottom edges

# Right Object Dimensions
r_plate_width = 50.0
r_plate_height = 35.0
r_plate_thick = 3.0

# Scene Layout
separation_x = 100.0
separation_z = -20.0
tilt_angle = 30.0  # Rotation around Y axis

# --- Left Object Construction ---
# Create the main vertical plate in the XZ plane
left_plate = cq.Workplane("XZ").box(l_plate_width, l_plate_height, l_plate_thick)

# Create the 3 pins attached to the left edge
# We define a workplane on the YZ plane (normal to X axis)
# and offset it to the left edge of the plate (-width/2)
pin_workplane = cq.Workplane("YZ").workplane(offset=-l_plate_width/2.0)

# Define pin locations (y=0 corresponds to center of thickness, z varies)
pin_locations = [
    (0, l_plate_height/2.0 - pin_margin_z),  # Top
    (0, 0),                                  # Middle
    (0, -l_plate_height/2.0 + pin_margin_z)  # Bottom
]

left_pins = (
    pin_workplane
    .pushPoints(pin_locations)
    .circle(pin_diameter / 2.0)
    .extrude(-pin_length)  # Extrude in negative X direction (away from plate)
)

# Combine plate and pins
left_obj = left_plate.union(left_pins)

# --- Right Object Construction ---
# Create the smaller plate
right_plate = cq.Workplane("XZ").box(r_plate_width, r_plate_height, r_plate_thick)

# Create the single pin attached to the left edge
right_pin_wp = cq.Workplane("YZ").workplane(offset=-r_plate_width/2.0)

right_pin = (
    right_pin_wp
    .center(0, 0)
    .circle(pin_diameter / 2.0)
    .extrude(-pin_length)
)

right_obj = right_plate.union(right_pin)

# --- Positioning ---
# Apply rotation and translation to the right object
# Rotate around Y axis to achieve the tilted look
right_obj = right_obj.rotate((0, 0, 0), (0, 1, 0), tilt_angle)
right_obj = right_obj.translate((separation_x, 0, separation_z))

# --- Final Result ---
result = left_obj.union(right_obj)