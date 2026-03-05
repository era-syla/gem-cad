import cadquery as cq

# Model Parameters
plate_width = 60.0      # Width of the square base plate
plate_height = 60.0     # Height of the square base plate
plate_thickness = 6.0   # Thickness of the base plate

rod_length = 100.0      # Length of the connecting rod
rod_diameter = 10.0     # Diameter of the connecting rod

flange_diameter = 40.0  # Diameter of the end circular flange
flange_thickness = 4.0  # Thickness of the end circular flange

# Hole Parameters
hole_offset_vertical = 18.0   # Distance from center to hole row height
hole_spacing = 15.0           # Horizontal distance from center to holes
dia_hole_small = 8.0          # Diameter of the smaller hole
dia_hole_large = 14.0         # Diameter of the larger hole

# 1. Create the Base Plate
# Oriented on the YZ plane to simulate a wall mount, extruding along X
result = cq.Workplane("YZ").box(plate_width, plate_height, plate_thickness)

# 2. Add Holes to the Base Plate
# Select the front face (>X)
# Coordinates: Local X maps to Global Y, Local Y maps to Global Z
result = (
    result.faces(">X")
    .workplane()
    # Small hole on the left (-Y direction)
    .pushPoints([(-hole_spacing, hole_offset_vertical)])
    .hole(dia_hole_small)
    # Large hole on the right (+Y direction)
    .faces(">X") # Re-select face after cut
    .workplane()
    .pushPoints([(hole_spacing, hole_offset_vertical)])
    .hole(dia_hole_large)
)

# 3. Create the Connecting Rod
# Extrude from the center of the base plate face
result = (
    result.faces(">X")
    .workplane()
    .center(0, 0)
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)

# 4. Create the End Flange
# Extrude from the end of the rod
result = (
    result.faces(">X")
    .workplane()
    .circle(flange_diameter / 2.0)
    .extrude(flange_thickness)
)

# 5. Add Cosmetic Detail to Flange Face
# Create a small recess in the center of the flange to represent the rod end/fastener
result = (
    result.faces(">X")
    .workplane()
    .circle(rod_diameter / 2.0)
    .cutBlind(-1.0) # Shallow cut
)