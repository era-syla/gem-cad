import cadquery as cq

# Create the main body of the vise
base = cq.Workplane("XY").box(60, 100, 20)

# Create the sliding jaw
sliding_jaw = cq.Workplane("XY").box(30, 20, 40).translate((0, 40, 20))

# Create the fixed jaw
fixed_jaw = cq.Workplane("XY").box(30, 20, 40).translate((0, -40, 20))

# Add a handle
handle = (
    cq.Workplane("XY")
    .cylinder(4, 80)
    .translate((10, 0, 60))
)

# Create the swivel base
swivel_base = (
    cq.Workplane("XY")
    .cylinder(5, 40)
    .translate((0, 0, -12))
)

# Assemble the components
result = base.union(sliding_jaw).union(fixed_jaw).union(handle).union(swivel_base)

# Fillet the main base edges
result = result.edges("|Z").fillet(2)