import cadquery as cq

# Parameters
length = 80
width = 40
height = 10

# Create main block
base = cq.Workplane("XY").box(length, width, height)

# Create a raised circular boss on the top surface
boss = (
    base.faces(">Z")
        .workplane()
        .pushPoints([(-length/4, 0)])
        .circle(10)
        .extrude(5)
)

# Create a conical pocket on the top surface
pocket = (
    base.faces(">Z")
        .workplane()
        .pushPoints([(length/4, 0)])
        .circle(10)                # top radius
        .workplane(offset=-7)      # pocket depth 7 mm into the block
        .circle(2)                 # bottom radius
        .loft(combine=False)
)

# Combine boss with base and subtract the pocket
model = base.union(boss).cut(pocket)

# Add a cylindrical pin on the right face
pin = (
    model.faces(">Y")
         .workplane()
         .circle(2.5)
         .extrude(20)
)

# Add a small triangular pointer on the top at the left end
tri = (
    cq.Workplane("XY")
      .workplane(offset=height)
      .center(-length/2, 0)
      .polyline([(0, 0), (0, 10), (10, 5)])
      .close()
      .extrude(5)
)

# Final result
result = model.union(pin).union(tri)