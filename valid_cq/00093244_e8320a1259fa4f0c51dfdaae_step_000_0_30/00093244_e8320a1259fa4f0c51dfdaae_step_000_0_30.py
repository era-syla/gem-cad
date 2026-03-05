import cadquery as cq

# -- Parametric Dimensions --
plate_length = 60.0
plate_height = 30.0
plate_thickness = 4.0
gap_width = 8.0          # Distance between the inner faces of the plates
fillet_radius = 5.0      # Radius for the top rounded corners
chamfer_size = 0.8       # Size of the chamfer on the outer faces
bridge_width = 8.0       # Width of the central connector along X
bridge_height = 8.0      # Height of the central connector along Z

# -- Geometry Construction --

# Helper function to generate the base shape of a side plate
def create_base_plate():
    # Initialize a box centered at the origin
    # Axis alignment: X=Length, Y=Thickness, Z=Height
    p = cq.Workplane("XY").box(plate_length, plate_thickness, plate_height)
    
    # Create the rounded top corners
    # Strategy: Select the top face (>Z) and then filter for edges parallel to Y (|Y)
    # This isolates the two short edges at the top of the plate's thickness
    p = p.faces(">Z").edges("|Y").fillet(fillet_radius)
    return p

# 1. Create the Front Plate
# Shift position to negative Y
y_offset_front = -(gap_width / 2.0 + plate_thickness / 2.0)
plate_front = create_base_plate().translate((0, y_offset_front, 0))

# Apply chamfer to the outer face
# The outer face is the one facing negative Y (<Y)
plate_front = plate_front.faces("<Y").edges().chamfer(chamfer_size)

# 2. Create the Back Plate
# Shift position to positive Y
y_offset_back = (gap_width / 2.0 + plate_thickness / 2.0)
plate_back = create_base_plate().translate((0, y_offset_back, 0))

# Apply chamfer to the outer face
# The outer face is the one facing positive Y (>Y)
plate_back = plate_back.faces(">Y").edges().chamfer(chamfer_size)

# 3. Create the Central Bridge
# A rectangular block connecting the two plates
# Its thickness (Y) matches the gap width exactly to bridge the space
bridge = cq.Workplane("XY").box(bridge_width, gap_width, bridge_height)

# 4. Final Boolean Union
# Combine both plates and the bridge into a single solid object
result = plate_front.union(plate_back).union(bridge)