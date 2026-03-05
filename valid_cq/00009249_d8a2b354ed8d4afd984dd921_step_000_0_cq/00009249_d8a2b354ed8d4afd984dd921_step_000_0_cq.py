import cadquery as cq

# --- Parametric Dimensions ---
width = 100.0       # Total width of the frame
height = 100.0      # Total height of the frame
thickness = 5.0     # Thickness of the plate
border_width = 10.0 # Width of the frame border

# --- 3D Modeling ---

# Method 1: Create a large rectangle and cut a smaller one
# result = (
#     cq.Workplane("XY")
#     .rect(width, height)
#     .extrude(thickness)
#     .faces(">Z")
#     .workplane()
#     .rect(width - 2*border_width, height - 2*border_width)
#     .cutBlind(-thickness)
# )

# Method 2: Create a sketch with two rectangles and extrude (more robust)
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2*border_width, height - 2*border_width)
    .extrude(thickness)
)

# Export or display the result (optional, but standard for these scripts)
# show_object(result)