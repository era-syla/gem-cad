import cadquery as cq

# Dimensions based on the image analysis
# This appears to be a pipe/funnel assembly with:
# - A narrow pipe section at top
# - A flared/funnel section at bottom
# - Rings/collars at connection points

# Main pipe (narrow cylindrical section)
pipe_outer_r = 8
pipe_inner_r = 6.5
pipe_height = 60

# Top cap/collar
top_collar_outer_r = 11
top_collar_inner_r = pipe_outer_r
top_collar_height = 5

# Top rim ring
top_rim_outer_r = 13
top_rim_inner_r = 10
top_rim_height = 8

# Funnel/flare section (bottom)
funnel_top_r = pipe_outer_r
funnel_bottom_r = 28
funnel_height = 25

# Bottom flange/base
base_outer_r = 32
base_inner_r = 26
base_height = 4

# Bottom collar ring
bottom_collar_outer_r = 30
bottom_collar_inner_r = 22
bottom_collar_height = 6

# Build the main pipe tube
main_pipe = (
    cq.Workplane("XY")
    .circle(pipe_outer_r)
    .circle(pipe_inner_r)
    .extrude(pipe_height)
)

# Top collar (wider section at top of pipe)
top_collar = (
    cq.Workplane("XY")
    .workplane(offset=pipe_height)
    .circle(top_collar_outer_r)
    .circle(pipe_inner_r)
    .extrude(top_collar_height)
)

# Top rim ring (decorative ring at top)
top_rim = (
    cq.Workplane("XY")
    .workplane(offset=pipe_height + top_collar_height - top_rim_height/2)
    .circle(top_rim_outer_r)
    .circle(top_rim_inner_r)
    .extrude(top_rim_height)
)

# Inner tube extending above collar
inner_tube_top = (
    cq.Workplane("XY")
    .workplane(offset=pipe_height + top_collar_height)
    .circle(pipe_inner_r - 0.5)
    .circle(pipe_inner_r - 2)
    .extrude(15)
)

# Funnel section - use revolve with a profile
# Create a shell funnel using loft approach
# Bottom funnel shell
funnel_outer = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(funnel_bottom_r)
    .workplane(offset=funnel_height)
    .circle(pipe_outer_r)
    .loft()
)

funnel_inner = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(funnel_bottom_r - 2)
    .workplane(offset=funnel_height)
    .circle(pipe_inner_r)
    .loft()
)

funnel_shell = funnel_outer.cut(funnel_inner)

# Bottom flat disk/base
base_disk = (
    cq.Workplane("XY")
    .circle(funnel_bottom_r)
    .extrude(3)
)

base_ring = (
    cq.Workplane("XY")
    .workplane(offset=3)
    .circle(base_outer_r)
    .circle(base_inner_r - 2)
    .extrude(base_height)
)

# Bottom collar ring (decorative)
bottom_ring = (
    cq.Workplane("XY")
    .workplane(offset=funnel_height - 4)
    .circle(bottom_collar_outer_r)
    .circle(bottom_collar_inner_r)
    .extrude(bottom_collar_height)
)

# Combine all parts
result = (
    main_pipe
    .union(top_collar)
    .union(top_rim)
    .union(inner_tube_top)
    .union(funnel_shell)
    .union(base_disk)
    .union(base_ring)
    .union(bottom_ring)
)