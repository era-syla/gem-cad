import cadquery as cq

# Parametric dimensions for the plate
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create the solid rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, centering logic can be explicit if needed, 
# but box() centers by default in CadQuery.
# To replicate the view, no rotation is strictly necessary as standard 
# iso views will show it angled.