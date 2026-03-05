import cadquery as cq

# Parameters
base_size = 100      # base square side length
top_radius = 35      # radius of the circular opening at top
height = 50          # height of the shape
wall_thickness = 5   # wall thickness

# Create the outer shell: pyramid-like shape transitioning from square base to circle top
# We'll do this by creating the outer solid and subtracting the inner void

# Outer solid: loft from square at bottom to circle at top
outer_bottom = (
    cq.Workplane("XY")
    .rect(base_size, base_size)
)

outer_top = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .circle(top_radius + wall_thickness)
)

outer_solid = (
    cq.Workplane("XY")
    .rect(base_size, base_size)
    .workplane(offset=height)
    .circle(top_radius + wall_thickness)
    .loft()
)

# Inner void: loft from slightly smaller square at bottom to circle at top
# The inner void removes material to create a hollow shell
inner_bottom_size = base_size - 2 * wall_thickness

inner_solid = (
    cq.Workplane("XY")
    .workplane(offset=0.01)  # slight offset to avoid boolean issues
    .rect(inner_bottom_size, inner_bottom_size)
    .workplane(offset=height - 0.01)
    .circle(top_radius)
    .loft()
)

# Subtract inner from outer
result = outer_solid.cut(inner_solid)