import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image proportions
head_diameter = 22.0      # Diameter of the large button head
head_thickness = 5.0      # Thickness of the head
shaft_diameter = 11.0     # Diameter of the main central shaft
shaft_length = 35.0       # Length of the main shaft
tip_diameter = 5.5        # Diameter of the small tip
tip_length = 8.0          # Length of the small tip
head_fillet = 2.0         # Fillet radius for the rounded head edge

# --- Modeling ---

# 1. Create the base Head geometry
# We start on the XY plane. The bottom face (at Z=0) will correspond 
# to the large rounded outer face of the pin.
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_thickness)

# 2. Add the Main Shaft
# Select the top flat face of the head and extrude the shaft cylinder.
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Add the Tip
# Select the top flat face of the shaft and extrude the smaller tip cylinder.
result = (
    result.faces(">Z")
    .workplane()
    .circle(tip_diameter / 2.0)
    .extrude(tip_length)
)

# 4. Refine Geometry
# Apply a fillet to the outer edge of the head (located at the bottom Z plane)
# to achieve the button-like appearance.
result = result.edges("<Z").fillet(head_fillet)

# Apply a small chamfer to the end of the tip for a realistic fastener finish.
result = result.faces(">Z").edges().chamfer(0.5)