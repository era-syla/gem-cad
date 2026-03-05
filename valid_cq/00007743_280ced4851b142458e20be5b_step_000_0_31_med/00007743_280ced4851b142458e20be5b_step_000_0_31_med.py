import cadquery as cq

# Define the base profile on the XZ plane (front view)
# This creates the inverted U-shape with tapered outer walls
profile_pts = [
    (-55, -50),
    (-60, 0),
    (60, 0),
    (55, -50),
    (25, -50),
    (25, -15),
    (-25, -15),
    (-25, -50)
]

# Extrude the profile along the Y-axis to create the main body block
result = cq.Workplane("XZ").polyline(profile_pts).close().extrude(40)

# Cut out the central gap from the front to form the two side legs
# The cut removes material from the front face (Y=40) inwards by 25mm, leaving the back bridge (Y=0 to 15)
result = result.faces(">Y").workplane().center(0, -25).rect(50, 50).cutBlind(-25)

# Add the stepped semi-circular arch cutouts on the bottom of the bridge
# The bridge bottom is at Z=-15
# Central through-hole
result = result.cut(cq.Workplane("XZ", origin=(0, 0, -15)).circle(10).extrude(15))
# Front counterbore
result = result.cut(cq.Workplane("XZ", origin=(0, 11, -15)).circle(13).extrude(4))
# Back counterbore
result = result.cut(cq.Workplane("XZ", origin=(0, 0, -15)).circle(13).extrude(4))

# Add the 4 mounting holes on the top face
top_holes = cq.Workplane("XY", origin=(0, 0, 0))
top_holes = top_holes.pushPoints([(-45, 7.5), (-35, 7.5), (35, 7.5), (45, 7.5)])
result = result.cut(top_holes.circle(3).extrude(-20))

# Add the 2 holes on the front face of each leg
front_holes = cq.Workplane("XZ", origin=(0, 40, 0))
front_holes = front_holes.pushPoints([(-40, -40), (40, -40)])
# Extrude backwards into the legs
result = result.cut(front_holes.circle(2.5).extrude(-15))

# Add prominent fillets to the bottom-outer edges of the legs
result = result.edges(cq.selectors.NearestToPointSelector((-55, 20, -50))).fillet(5)
result = result.edges(cq.selectors.NearestToPointSelector((55, 20, -50))).fillet(5)