import cadquery as cq

# Create the base cylinder
base = cq.Workplane("XY").circle(10).extrude(20)

# Create the vertical rectangular part
rect_part = base.faces(">Z").workplane().rect(15, 40).extrude(5)

# Create the rounded top
top_profile = rect_part.faces(">Z").workplane().center(0, 7.5).rect(15, 25, centered=(True, False)).extrude(10)
rounded_top = top_profile.faces(">Z").workplane().center(0, 12.5).circle(7.5).cutThruAll()

# Create the hole in the rounded top
result = rounded_top.faces(">Z").workplane().center(0, 12.5).hole(5)

# Final result with the cutout for the lower portion
result = result.faces("<Z").workplane().rect(10, 10).cutBlind(-20)