import cadquery as cq

# Parameters
outer_r = 6.5
inner_r = 5.0
pipe_length = 15.0
flare_length = 60.0
sheet_width = 80.0
sheet_thickness = outer_r - inner_r

# Build the transition from a hollow tube to a flat sheet
result = (
    cq.Workplane("XY")
    # starting ring (outer and inner) at z=0
    .circle(outer_r)
    .circle(inner_r)
    # repeat the ring at z=pipe_length to create a straight tube section
    .workplane(offset=pipe_length)
    .circle(outer_r)
    .circle(inner_r)
    # at z=pipe_length + flare_length, place the sheet profile (single rectangle)
    .workplane(offset=flare_length)
    .rect(sheet_width, sheet_thickness)
    # loft through all three sections, closing the inner hole at the sheet end
    .loft()
)