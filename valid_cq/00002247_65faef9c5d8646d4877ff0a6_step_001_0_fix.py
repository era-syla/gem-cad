import cadquery as cq

# Dimensions
outer_length = 160
outer_width = 60
outer_height = 70
wall_thickness = 3
bottom_thickness = 3

# Draft angle for tapered walls (inward taper)
draft_angle = 5  # degrees
import math

# Calculate inner dimensions at top (wider due to draft)
taper = outer_height * math.tan(math.radians(draft_angle))

inner_length_bottom = outer_length - 2 * wall_thickness
inner_width_bottom = outer_width - 2 * wall_thickness
inner_length_top = inner_length_bottom + 2 * taper
inner_width_top = inner_width_bottom + 2 * taper

# Build the outer box
outer_box = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)

# Build the inner tapered cavity using loft
inner_cavity = (
    cq.Workplane("XY")
    .workplane(offset=bottom_thickness)
    .rect(inner_length_bottom, inner_width_bottom)
    .workplane(offset=outer_height - bottom_thickness)
    .rect(inner_length_top, inner_width_top)
    .loft()
)

# Subtract cavity from box
tub = outer_box.cut(inner_cavity)

# Add a flange/lip on one short end (left side)
flange_width = 15
flange_thickness = wall_thickness
flange_height = outer_height * 0.6

flange = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=cq.Vector(-outer_length / 2 - flange_width / 2, 0, flange_height / 2 - outer_height / 2))
    .rect(flange_width, outer_width + 2 * flange_thickness)
    .extrude(flange_height)
)

# Actually build the flange properly
flange = (
    cq.Workplane("XY")
    .box(flange_width, outer_width + 2 * flange_thickness, flange_height,
         centered=(True, True, False))
    .translate((-outer_length / 2 - flange_width / 2, 0, 0))
)

result = tub.union(flange)