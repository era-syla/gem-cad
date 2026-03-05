import cadquery as cq

# Parametric Dimensions
shaft_diameter = 8.0
shaft_length = 50.0
head_diameter = 13.0
head_height = 6.0
chamfer_size = 0.5
text_string = "8-50"
text_size = 4.0
text_extrusion = 0.5

# 1. Create the Head
# Extrude circle upwards from the XY plane
head = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Create the Shaft
# Extrude circle downwards from the XY plane
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(-shaft_length)

# 3. Create the Main Body
# Union the head and shaft
pin_body = head.union(shaft)

# 4. Add Detail: Chamfer the bottom of the shaft
# Select the face with the lowest Z value, then select its edges
pin_body = pin_body.faces("<Z").edges().chamfer(chamfer_size)

# 5. Add Detail: Embossed Text
# Select the top face of the head
# Create a workplane and rotate it 45 degrees to match the image orientation
top_workplane = pin_body.faces(">Z").workplane().transformed(rotate=(0, 0, 45))

# Generate the text solid
text_solid = top_workplane.text(text_string, fontsize=text_size, distance=text_extrusion)

# 6. Final Result
# Union the text with the pin body
result = pin_body.union(text_solid)