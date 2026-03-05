import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Overall diameter of the disc
thickness = 5.0         # Total thickness of the disc
rim_width = 15.0        # Width of the outer rim
recess_depth = 2.0      # Depth of the central recess

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - rim_width
base_thickness = thickness - recess_depth

# Create the main body
# Start with the full cylinder
result = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# Create the recess by cutting a smaller cylinder from the top
# Move workplane to the top face
result = result.faces(">Z").workplane() \
    .circle(inner_radius) \
    .cutBlind(-recess_depth)

# Alternative approach (additive):
# 1. Create the base thin disc
# 2. Add the rim on top
# base = cq.Workplane("XY").circle(outer_radius).extrude(base_thickness)
# rim = cq.Workplane("XY").workplane(offset=base_thickness)\
#        .circle(outer_radius).circle(inner_radius).extrude(recess_depth)
# result = base.union(rim)

# Ensure the 'result' variable is available
if 'show_object' in globals():
    show_object(result)