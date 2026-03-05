import cadquery as cq

# --- Parametric Dimensions ---
total_length = 100.0    # Total length of the rod
diameter = 16.0         # Diameter of the rod
thread_length = 30.0    # Length of the threaded portion
chamfer_size = 1.0      # Size of the end chamfers

# --- Modeling ---

# 1. Create the unthreaded shank section
# We define the shank length based on total and thread lengths
shank_length = total_length - thread_length

# Create the base shank cylinder on the YZ plane, extruding along the X axis
shank = (
    cq.Workplane("YZ")
    .circle(diameter / 2.0)
    .extrude(shank_length)
)

# 2. Create the threaded section
# We continue from the end of the shank to create the threaded portion.
# While actual helical threads are computationally expensive and typically 
# omitted in CAD solids, we model the cylindrical envelope here.
# Extruding from the face automatically performs a boolean union.
result = (
    shank.faces(">X")
    .workplane()
    .circle(diameter / 2.0)
    .extrude(thread_length)
)

# 3. Apply Chamfers
# Standard studs have chamfers on both ends to aid assembly and prevent damage.
# We select the faces at the extreme negative and positive X coordinates.
result = result.faces("<X or >X").chamfer(chamfer_size)