import cadquery as cq

# Parameters
t = 3               # plate thickness
w = 20              # bracket width
h_leg = 30          # horizontal leg length
v_leg = 60          # vertical leg height
hole_size = 5       # square hole size
n_top = 4           # number of holes on top face
n_cols = 4          # number of columns of holes on side face
n_rows = 5          # number of rows of holes on side face
gap = 20            # gap between brackets (connector length)

# Create one L‐shaped bracket
bracket = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (h_leg, 0),
          (h_leg, t),
          (t, t),
          (t, v_leg),
          (0, v_leg)
      ])
      .close()
      .extrude(w)
)

# Drill square holes on top face
spacing_top = (h_leg - 2 * hole_size) / (n_top - 1)
x_pos_top = [hole_size + i * spacing_top for i in range(n_top)]
bracket = (
    bracket
      .faces(">Z")
      .workplane()
      .pushPoints([(x, 0) for x in x_pos_top])
      .rect(hole_size, hole_size)
      .cutThruAll()
)

# Drill square holes on front vertical face
spacing_z = (v_leg - 2 * hole_size - t) / (n_rows - 1)
z_pos = [t + hole_size + j * spacing_z for j in range(n_rows)]
spacing_y = (w - 2 * hole_size) / (n_cols - 1)
y_pos = [-w/2 + hole_size + i * spacing_y for i in range(n_cols)]
bracket = (
    bracket
      .faces(">X")
      .workplane()
      .pushPoints([(y, z) for z in z_pos for y in y_pos])
      .rect(hole_size, hole_size)
      .cutThruAll()
)

# Create the connector between brackets
connector = (
    cq.Workplane("XY")
      .box(t, w, gap)
      .translate((t/2, 0, -gap/2))
)

# Mirror the bracket to make the lower one
bracket_mirror = bracket.mirror(mirrorPlane="XY", basePointVector=(0, 0, 0))

# Combine everything
result = bracket.union(bracket_mirror).union(connector)