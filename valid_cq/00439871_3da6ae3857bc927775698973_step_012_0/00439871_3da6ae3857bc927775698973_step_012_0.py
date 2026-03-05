import cadquery as cq

# --- Parametric Dimensions ---
head_width = 25.0       # Width/Height of the square head
head_thickness = 6.0    # Thickness of the square head
shaft_diameter = 10.0   # Major diameter of the threaded shaft
shaft_length = 50.0     # Length of the shaft
hole_diameter = 5.0     # Diameter of the central through-hole
chamfer_size = 0.75     # Size of chamfers for edges

# --- 3D Modeling ---

# 1. Create the Square Head
# Centered on the XY plane.
result = cq.Workplane("XY").box(head_width, head_width, head_thickness)

# 2. Add the Cylindrical Shaft
# Select the top face (>Z) of the square head and extrude the shaft.
# Note: Threads are represented by the major diameter cylinder (standard CAD practice).
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Chamfer the End of the Shaft
# Applied before the hole is cut to easily select the outer edge of the shaft top.
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# 4. Create the Center Through-Hole
# Creates a hole through the entire assembly (head and shaft).
result = (
    result
    .faces("<Z")
    .workplane()
    .hole(hole_diameter)
)

# 5. Chamfer the Hole Opening on the Square Head
# Select the bottom face (<Z), then filter for the circular edge of the hole.
result = (
    result
    .faces("<Z")
    .edges("%Circle")
    .chamfer(chamfer_size)
)

# The 'result' variable now contains the final solid geometry.