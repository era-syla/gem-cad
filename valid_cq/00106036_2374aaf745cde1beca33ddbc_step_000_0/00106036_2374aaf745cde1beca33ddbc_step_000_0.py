import cadquery as cq

# Parameters for the geometry
length = 120.0        # Total length of the plate
height = 50.0         # Total height of the plate
thickness = 3.0       # Plate thickness
corner_radius = 4.0   # Radius of the plate corners

# Vertical slot parameters (on the sides)
v_slot_w = 4.0        # Width of vertical slots
v_slot_h = 20.0       # Height (length) of vertical slots
v_slot_offset = 52.0  # Distance from center to vertical slot center (X axis)

# Horizontal slot parameters (at the bottom)
h_slot_w = 25.0       # Length of horizontal slots
h_slot_h = 4.0        # Height (width) of horizontal slots
h_slot_dist_x = 30.0  # Distance from center to horizontal slot center (X axis)
h_slot_offset_y = 16.0 # Distance from center to horizontal slot center (Y axis - downwards)

# Create the base plate centered at origin
result = cq.Workplane("XY").box(length, height, thickness)

# Fillet the four vertical corners
result = result.edges("|Z").fillet(corner_radius)

# Cut the two vertical slots on the left and right sides
# We push points to the locations and cut rectangles
result = (result.faces(">Z").workplane()
          .pushPoints([(-v_slot_offset, 0), (v_slot_offset, 0)])
          .rect(v_slot_w, v_slot_h)
          .cutThruAll())

# Cut the two horizontal slots near the bottom edge
# Note: h_slot_offset_y is applied downwards relative to the center
result = (result.faces(">Z").workplane()
          .pushPoints([(-h_slot_dist_x, -h_slot_offset_y), 
                       (h_slot_dist_x, -h_slot_offset_y)])
          .rect(h_slot_w, h_slot_h)
          .cutThruAll())