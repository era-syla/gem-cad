import cadquery as cq

# Parameters
length = 200.0  # total length of the bar
width = 12.0    # width of the bar
thickness = 3.0 # thickness of the bar
hole_d = 5.0    # diameter of each hole
n_holes = 10    # number of holes
pitch = 20.0    # center-to-center distance between holes
end_margin = pitch/2.0  # distance from the bar end to first hole center

# Compute hole positions along the length
y_positions = [ -length/2 + end_margin + i*pitch for i in range(n_holes) ]
hole_points = [(0, y) for y in y_positions]

# Build the part
result = (
    cq.Workplane("XY")
      .rect(width, length)
      .extrude(thickness)
      .faces(">Z")
      .workplane()
      .pushPoints(hole_points)
      .hole(hole_d)
)