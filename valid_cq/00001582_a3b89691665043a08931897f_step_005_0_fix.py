import cadquery as cq

# Main plate dimensions
plate_w = 80
plate_d = 80
plate_h = 8

# Tab dimensions
tab_w = 10
tab_d = 6
tab_h = 6

# Center hole
center_hole_r = 7

# Small holes offset from center
small_hole_r = 2
small_hole_offset = 15

# Build the main plate
result = (
    cq.Workplane("XY")
    .rect(plate_w, plate_d)
    .extrude(plate_h)
)

# Add tabs on all four sides (two tabs per side, symmetric)
# The tabs protrude from the bottom portion of the plate
tab_z_offset = 0  # tabs start at bottom
tab_height = tab_h  # same as plate_h - some offset

# Tab positions along each side
tab_offset_along = 20  # offset from center along the side

# Bottom side tabs (Y = -plate_d/2)
for sign in [-1, 1]:
    result = (
        result
        .union(
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(sign * tab_offset_along, -plate_d/2 - tab_d/2, 0))
            .rect(tab_w, tab_d)
            .extrude(tab_height)
        )
    )

# Top side tabs (Y = +plate_d/2)
for sign in [-1, 1]:
    result = (
        result
        .union(
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(sign * tab_offset_along, plate_d/2 + tab_d/2, 0))
            .rect(tab_w, tab_d)
            .extrude(tab_height)
        )
    )

# Left side tabs (X = -plate_w/2)
for sign in [-1, 1]:
    result = (
        result
        .union(
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(-plate_w/2 - tab_d/2, sign * tab_offset_along, 0))
            .rect(tab_d, tab_w)
            .extrude(tab_height)
        )
    )

# Right side tabs (X = +plate_w/2)
for sign in [-1, 1]:
    result = (
        result
        .union(
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(plate_w/2 + tab_d/2, sign * tab_offset_along, 0))
            .rect(tab_d, tab_w)
            .extrude(tab_height)
        )
    )

# Cut the center hole through the plate
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(center_hole_r * 2)
)

# Cut small holes around the center
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (small_hole_offset, 0),
        (-small_hole_offset, 0),
        (0, small_hole_offset),
        (0, -small_hole_offset),
    ])
    .hole(small_hole_r * 2)
)