import cadquery as cq

# Parametric dimensions
base_width = 100.0   # Width of the bottom base block
base_depth = 100.0   # Depth of the bottom base block
base_height = 50.0   # Height of the bottom base block

top_width = 60.0     # Width of the top block
top_depth = 60.0     # Depth of the top block
top_height = 40.0    # Height of the top block without fillet
top_fillet = 10.0    # Radius of the fillet on the top edges

# Create the base block
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# Create the top block
# We create a new workplane on the top face of the base and extrude/box the top part
# Since box() creates a centered solid by default, we can simply union a new box 
# that is shifted up to sit on top of the base.
top = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2 + top_height / 2)
    .box(top_width, top_depth, top_height)
)

# Combine the parts
result = base.union(top)

# Apply fillet to the top edges of the top block
# We select the top face (which has the highest Z value) and fillet its edges
result = result.faces(">Z").edges().fillet(top_fillet)
