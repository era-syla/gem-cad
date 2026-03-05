import cadquery as cq

# Parametric dimensions
# Estimating dimensions based on typical proportions for a pin like this
pin_diameter = 5.0     # Diameter of the main shaft
pin_length = 50.0      # Length of the main shaft
head_diameter = 8.0    # Diameter of the head
head_thickness = 4.0   # Thickness (length) of the head
chamfer_size = 0.5     # Size of the chamfer at the end of the pin

# Create the main shaft
# We start with a cylinder for the shaft
shaft = cq.Workplane("XY").circle(pin_diameter / 2).extrude(pin_length)

# Create the head
# We create a new workplane on the top face of the shaft and extrude the head
# Alternatively, we can just build it at the base. Let's build it at the base (Z=0) going downwards or upwards.
# Let's start from Z=0 going up for shaft, and Z=0 going down for head to keep it simple,
# or just stack them.

# Approach:
# 1. Create Head cylinder
# 2. Create Shaft cylinder on top of it
# 3. Chamfer the end of the shaft

# Create the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_thickness)

# Create the shaft on top of the head
# We select the top face of the head (the face with highest Z value)
shaft = (
    head.faces(">Z")
    .workplane()
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# Add chamfer to the end of the shaft
# Select the edge at the very top of the shaft (highest Z)
result = (
    shaft.faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Optional: Add a small fillet between head and shaft for realism/strength, 
# typically found on manufactured parts, though not strictly visible in the low-res image.
# Let's stick to the visible geometry which is fairly sharp, but a small fillet is good practice.
# result = result.edges(cq.selectors.NearestToPointSelector((0, 0, head_thickness))).fillet(0.2)

# Final result is stored in 'result' variable