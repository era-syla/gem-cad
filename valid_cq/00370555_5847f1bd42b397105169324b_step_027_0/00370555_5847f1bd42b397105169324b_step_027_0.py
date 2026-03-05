import cadquery as cq

# -- Parametric Dimensions --
height = 30.0
thickness = 3.0
web_length = 60.0
left_flange_length = 22.0
right_flange_length = 8.0
slot_length = 35.0
slot_width = 5.0
hole_diameter = 4.0
hole_spacing = 14.0
fillet_radius = 3.0

# -- Model Construction --

# 1. Base Shape: Extruded C-Profile
# Create the profile on the XY plane and extrude along Z.
# Orientation:
# - Web runs along the X-axis.
# - Flanges run along the +Y axis.
# - Origin (0,0) is at the outer corner of the left flange (where it meets the web).
result = (
    cq.Workplane("XY")
    .moveTo(0, left_flange_length)
    .lineTo(0, 0)                      # Left outer corner
    .lineTo(web_length, 0)             # Right outer corner
    .lineTo(web_length, right_flange_length)
    .lineTo(web_length - thickness, right_flange_length)
    .lineTo(web_length - thickness, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, left_flange_length)
    .close()
    .extrude(height)
)

# 2. Fillet the right outer corner
# Select the vertical edge at the far right end of the web (approx X=web_length, Y=0)
# Using a selector to find the edge nearest to that geometric point.
result = result.edges(
    cq.selectors.NearestToPointSelector((web_length, 0, height / 2))
).fillet(fillet_radius)

# 3. Cut the Slot in the Web
# Select the outer face of the web (Plane Y=0)
# The workplane center defaults to the center of the selected face bounding box.
result = (
    result.faces("<Y")
    .workplane()
    .slot2D(slot_length, slot_width)
    .cutBlind(-thickness * 2)  # Cut into the material (negative direction relative to face normal)
)

# 4. Cut Mounting Holes in Left Flange
# Select the outer face of the left flange (Plane X=0)
# The workplane center defaults to the center of the face (vertically centered at height/2).
result = (
    result.faces("<X")
    .workplane()
    .pushPoints([(0, hole_spacing / 2), (0, -hole_spacing / 2)])
    .circle(hole_diameter / 2)
    .cutBlind(-thickness * 2)
)