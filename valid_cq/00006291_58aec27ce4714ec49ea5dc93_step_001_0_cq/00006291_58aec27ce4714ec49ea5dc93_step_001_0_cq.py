import cadquery as cq

# Parametric dimensions
# Main cylinder (body) dimensions
body_outer_diameter = 20.0
body_length = 5.0

# Flange dimensions
flange_outer_diameter = 25.0
flange_thickness = 1.5

# Through hole dimension
inner_diameter = 16.0

# Create the main body cylinder
# We start by creating the body
body = cq.Workplane("XY").circle(body_outer_diameter / 2.0).extrude(body_length)

# Create the flange
# The flange is located at one end of the body. Let's put it at the "bottom" (Z=0 plane)
# Since the body was extruded upwards from XY plane, the bottom face is on XY.
# We can just create a larger cylinder at the same location with the flange thickness.
flange = cq.Workplane("XY").circle(flange_outer_diameter / 2.0).extrude(flange_thickness)

# Union the body and the flange
part = body.union(flange)

# Create the through hole
# We cut a cylinder through the entire part
result = part.faces(">Z").workplane().hole(inner_diameter)

# Alternatively, a more efficient single-operation approach using a revolution:
# 1. Define the cross-section profile
# 2. Revolve it around the Z axis

# Let's refine the first approach slightly to be cleaner with a single workplane stack if possible, 
# but the union approach is very robust for readability.

# Let's verify the orientation. The image shows the flange on the "front" or top, 
# and the body extending backwards. Let's adjust to match the visual better.
# The previous code puts flange at Z=0 and body extending to Z=5.
# Let's make it so the flange is the visible top surface.

# Revised Approach:
# 1. Create the flange.
# 2. Add the body extending from the back of the flange.
# 3. Cut the hole.

# Dimensions (Refined estimates based on visual proportions)
ID = 30.0  # Inner Diameter
OD_body = 34.0 # Body Outer Diameter
OD_flange = 40.0 # Flange Outer Diameter
L_flange = 2.0 # Flange thickness
L_body = 8.0 # Total length or length of the body section

# Creating the shape
result = (
    cq.Workplane("XY")
    # Create the flange base
    .circle(OD_flange / 2.0)
    .extrude(L_flange)
    # Select the top face of the flange to extrude the body from, 
    # but looking at the image, the flange seems to be the "rim". 
    # Let's extrude the body from the *back* of the flange to keep the flange as the reference plane
    .faces("<Z") 
    .workplane()
    .circle(OD_body / 2.0)
    .extrude(L_body - L_flange) # Extrude the remaining length
    # Now cut the through hole through everything
    .faces(">Z") # Select the very top face (back of the body now)
    .workplane() 
    .hole(ID)
)

# Wait, looking at the image, the flange is closer to the viewer.
# Let's try constructing it simply as two cylinders unioned, then drilled.
# This is often the most robust way to ensure parameters work as expected.

# Final Code Structure
part_body = cq.Workplane("XY").circle(OD_body/2).extrude(L_body)
part_flange = cq.Workplane("XY").circle(OD_flange/2).extrude(L_flange)

# Combine and cut hole. 
# Note: Since both start at Z=0 on XY, the flange overlaps the start of the body.
# This matches a "rim" geometry perfectly.
result = part_body.union(part_flange).faces(">Z").workplane().hole(ID)