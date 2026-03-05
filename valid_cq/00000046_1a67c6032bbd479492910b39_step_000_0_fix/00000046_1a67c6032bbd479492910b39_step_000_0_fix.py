import cadquery as cq

# Parameters
plate_w = 120.0     # plate width in X
plate_h = 150.0     # plate height in Y
plate_t = 3.0       # plate thickness in Z

grid_w = 80.0       # grid square width in X
grid_h = 80.0       # grid square height in Y
cols = 40           # number of pins in X
rows = 40           # number of pins in Y

pin_d = 1.0         # pin diameter
pin_h = 2.0         # pin height

margin_bottom = 20.0              # distance from bottom of plate to bottom of grid
margin_x = (plate_w - grid_w)/2.0 # center grid horizontally

# Compute spacing and start point
spacing_x = grid_w/(cols - 1)
spacing_y = grid_h/(rows - 1)
x_start = -plate_w/2 + margin_x
y_start = -plate_h/2 + margin_bottom

# Generate grid of points
points = [
    (x_start + i*spacing_x, y_start + j*spacing_y)
    for i in range(cols)
    for j in range(rows)
]

# Build model
result = (
    cq.Workplane("XY")
      .box(plate_w, plate_h, plate_t)
      .faces(">Z")
      .workplane()
      .pushPoints(points)
      .circle(pin_d/2)
      .extrude(pin_h)
)