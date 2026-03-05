import cadquery as cq

# Parametric dimensions
length = 100.0    # Length of the rectangular plate
width = 60.0      # Width of the rectangular plate
thickness = 5.0   # Thickness of the plate
hole_diameter = 20.0 # Diameter of the central hole

# Create the part
# 1. Start with a box centered on the XY plane
# 2. Select the top face (positive Z direction)
# 3. Create a workplane on that face
# 4. Cut a hole through the entire part
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)