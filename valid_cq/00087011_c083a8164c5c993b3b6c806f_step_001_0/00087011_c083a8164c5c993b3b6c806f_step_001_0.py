import cadquery as cq

# Parametric dimensions for the gear rack / rail
length = 250.0       # Total length of the rail
width = 15.0         # Width of the rail
height = 15.0        # Height of the rail
groove_width = 5.0   # Width of the top guide slot
groove_depth = 5.0   # Depth of the top guide slot
tooth_pitch = 12.0   # Distance between teeth (pitch)
tooth_cut_w = 6.0    # Width of the material removed for each tooth
tooth_cut_d = 4.0    # Depth of the tooth cut

# 1. Create the base block
# Centered at the origin
result = cq.Workplane("XY").box(length, width, height)

# 2. Create the top longitudinal groove
# Select the top face (+Z), draw a rectangle the full length of the part, and cut down
result = result.faces(">Z").workplane() \
    .rect(length, groove_width) \
    .cutBlind(-groove_depth)

# 3. Create the bottom rack teeth
# Select the bottom face (-Z) and create an array of cuts
# Calculate the number of notches that fit along the length
num_notches = int(length / tooth_pitch)

result = result.faces("<Z").workplane() \
    .rarray(xSpacing=tooth_pitch, ySpacing=1, xCount=num_notches, yCount=1, center=True) \
    .rect(tooth_cut_w, width * 2.0) \
    .cutBlind(-tooth_cut_d)