import cadquery as cq

# Parameters
L = 60.0            # length of the block
w = 20.0            # width (depth) of extrusion
h_end = 10.0        # height at both front and back ends
h_peak = 15.0       # peak height of the top arc at mid-length
r_cut = 5.0         # radius of semicircular cutouts at the bottom ends
d_cut = 10.0        # distance from each end to the center of the cutout
lug_depth = 6.0     # extension of each lug in the X direction
lug_width = 4.0     # width of each lug in the Y direction
lug_height = 5.0    # height of each lug in the Z direction
lug_sep = 6.0       # offset of each lug from the centerline in Y

# Build the main curved body
result = (
    cq.Workplane("XZ")
      .moveTo(0, 0)
      .lineTo(0, h_end)
      .threePointArc((L/2, h_peak), (L, h_end))
      .lineTo(L, 0)
      .close()
      .extrude(w)
)

# Cut semicircular slots at the bottom ends
result = result.cut(
    cq.Workplane("XZ")
      .center(d_cut, r_cut)
      .circle(r_cut)
      .extrude(w)
).cut(
    cq.Workplane("XZ")
      .center(L - d_cut, r_cut)
      .circle(r_cut)
      .extrude(w)
)

# Add two small lugs on top near the back
# First lug on the positive Y side
result = result.faces(">Z").workplane().center(L - lug_depth/2, lug_sep).rect(lug_depth, lug_width).extrude(lug_height)
# Second lug on the negative Y side
result = result.faces(">Z").workplane().center(L - lug_depth/2, -lug_sep).rect(lug_depth, lug_width).extrude(lug_height)