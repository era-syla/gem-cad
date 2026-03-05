import cadquery as cq

# L-bracket angle iron
# Dimensions
length = 120
flange_width = 30
web_height = 25
thickness = 3

# Create the L-profile by extruding an L-shaped cross section
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(flange_width, 0)
    .lineTo(flange_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, web_height)
    .lineTo(0, web_height)
    .close()
)

result = profile.extrude(length)

# Add holes in the horizontal flange
# 4 holes along the length, positioned in the flange
hole_diameter = 5
hole_depth = thickness + 2

# Holes on the horizontal flange (bottom face of the flange)
# The flange lies in the XY plane at Z=0 to Z=thickness
# We need to drill from the top of the flange downward
# Flange top surface is at y=thickness in YZ plane, extruded along X

# Work on the top face of the horizontal flange
# In the extruded solid, X goes 0 to length, flange is at Z=0 to thickness (in world coords)
# Let's add holes on the flange top surface

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (20, flange_width/2 - thickness/2 - 5),
        (45, flange_width/2 - thickness/2 - 5),
        (75, flange_width/2 - thickness/2 - 5),
        (100, flange_width/2 - thickness/2 - 5),
    ])
    .hole(hole_diameter)
)

# Add holes on the vertical web face
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([
        (20, web_height/2),
        (60, web_height/2),
        (100, web_height/2),
    ])
    .hole(hole_diameter)
)