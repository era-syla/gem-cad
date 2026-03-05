import cadquery as cq

# --- Parametric Dimensions ---
# Based on the visual proportions of the image
length = 100.0  # The horizontal length
height = 60.0   # The vertical height
thickness = 5.0 # The thickness of the plate

# --- 3D Model Construction ---
# Create a simple box centered on the XY plane.
# This creates the basic rectangular plate shown in the image.
result = cq.Workplane("XY").box(length, thickness, height)

# Alternatively, if you prefer the thickness to be along the Y-axis and standing up on Z:
# result = cq.Workplane("XY").box(length, thickness, height)
# This results in:
# - Length along X
# - Thickness along Y
# - Height along Z