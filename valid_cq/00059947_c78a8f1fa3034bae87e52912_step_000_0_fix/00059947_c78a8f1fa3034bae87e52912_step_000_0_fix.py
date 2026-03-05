import cadquery as cq

# Define the triangular profile in the X–Z plane
tri_pts = [(0, 0), (120, 0), (40, 90)]

# Extrude the triangle along Y to form a prism
result = (
    cq.Workplane("XZ")
      .polyline(tri_pts)
      .close()
      .extrude(20)
)