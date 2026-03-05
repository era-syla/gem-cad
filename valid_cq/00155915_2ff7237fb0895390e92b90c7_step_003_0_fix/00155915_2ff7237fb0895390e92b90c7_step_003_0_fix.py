import cadquery as cq

# Parameters
r = 10           # radius of bottom semicircle
side_h = 15      # height of the side edges from the base of the semicircle
top_w = 8        # width of the flat top edge
thickness = 5    # extrusion thickness

# Build the profile: semicircle + two straight edges + flat top
result = (
    cq.Workplane("XY")
      .moveTo(r, 0)
      .threePointArc((0, -r), (-r, 0))
      .lineTo(-top_w/2, side_h)
      .lineTo( top_w/2, side_h)
      .close()
      .extrude(thickness)
)