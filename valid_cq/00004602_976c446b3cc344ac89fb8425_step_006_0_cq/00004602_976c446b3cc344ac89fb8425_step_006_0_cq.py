import cadquery as cq

# Parametric dimensions
base_length = 100.0  # Length of the bottom flange
base_width = 70.0    # Width of the bottom flange
base_thickness = 5.0 # Thickness of the bottom flange

top_length = 90.0    # Length of the main block
top_width = 60.0     # Width of the main block
top_height = 20.0    # Height of the main block above the flange

# Create the model
# Step 1: Create the bottom flange (base)
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Step 2: Create the top block on top of the base
# We select the top face of the base and draw the rectangle for the top block
# box() centers the object, so we need to offset it to sit on top
# Alternatively, we can just create a second box and union them. 
# A cleaner way in CQ is usually to select a face and extrude, or just union two boxes positioned correctly.

# Method: Union of two boxes positioned relative to global origin
# Let's assume the origin is at the center of the bottom face of the base.
# Base center is at (0,0, base_thickness/2)
# Top block center is at (0,0, base_thickness + top_height/2)

top_block = cq.Workplane("XY").workplane(offset=base_thickness/2).box(top_length, top_width, top_height)

# The base was created centered at Z=0. Let's adjust to make z=0 the bottom.
# Re-creating with a more stacking-friendly approach.

result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness) # Create base centered at (0,0,0)
    .faces(">Z") # Select top face
    .workplane() 
    .rect(top_length, top_width) # Sketch rectangle for top block
    .extrude(top_height) # Extrude upwards
)

# Export the result if needed, or just leave it in the 'result' variable as requested
if __name__ == "__main__":
    try:
        from cadquery import exporters
        exporters.export(result, "stepped_block.step")
    except ImportError:
        pass