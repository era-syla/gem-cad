import cadquery as cq

# Parametric dimensions for the stepped shaft model
# Estimated dimensions in mm based on visual proportions

# Section 1: Head/Collar (Rightmost section)
d_head = 18.0
l_head = 12.0

# Section 2: Large Shaft Section
d_large = 14.0
l_large = 65.0

# Section 3: Medium Shaft Section
d_medium = 10.0
l_medium = 65.0

# Section 4: Small Shaft Section (Tip/Leftmost)
d_small = 6.0
l_small = 30.0

# Generate the model
# Building along the X-axis to match the horizontal orientation
result = (
    cq.Workplane("YZ")
    # Create the Head
    .circle(d_head / 2.0)
    .extrude(l_head)
    
    # Create the Large Section
    .faces(">X").workplane()
    .circle(d_large / 2.0)
    .extrude(l_large)
    
    # Create the Medium Section
    .faces(">X").workplane()
    .circle(d_medium / 2.0)
    .extrude(l_medium)
    
    # Create the Small Section (Tip)
    .faces(">X").workplane()
    .circle(d_small / 2.0)
    .extrude(l_small)
)