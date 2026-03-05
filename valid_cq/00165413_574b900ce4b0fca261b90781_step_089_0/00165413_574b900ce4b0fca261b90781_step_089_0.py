import cadquery as cq

# -- Parametric Dimensions --
# Dimensions estimated from the image to maintain proportions
head_diameter = 25.0
head_length = 15.0
shaft_diameter = 12.5
shaft_length = 45.0

head_chamfer_size = 1.0   # Chamfer on the back of the head
shaft_chamfer_size = 1.0  # Chamfer on the tip of the shaft
neck_fillet_radius = 2.5  # Fillet at the transition

# -- Modeling Process --

# 1. Create the Head
# Start on the XY plane and extrude the larger cylinder
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_length)

# 2. Create the Shaft
# Select the top face of the head (max Z) and extrude the smaller cylinder
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Apply Features
# Chamfer the bottom edge of the head (at Z=0)
result = result.edges("<Z").chamfer(head_chamfer_size)

# Chamfer the top edge of the shaft (at the very end of the part)
result = result.edges(">Z").chamfer(shaft_chamfer_size)

# Fillet the transition neck between head and shaft
# We locate the edge by selecting the edge nearest to the center point at the height of the head
neck_location = (0, 0, head_length)
result = result.edges(cq.selectors.NearestToPointSelector(neck_location)).fillet(neck_fillet_radius)