import cadquery as cq

# Parameters for the 2020-style aluminum extrusion profile
w = 20.0        # Profile width/height
sw = 6.0        # Slot width
sd = 5.0        # Slot depth
hd = 5.0        # Center hole diameter

# Lengths of the structural members
len_z_up = 360.0
len_z_down = 80.0
len_x = 280.0
len_y = 200.0

# Create the 2D sketch for the extrusion cross-section
extrusion_sketch = (
    cq.Sketch()
    .rect(w, w)
    # Cut top and bottom slots
    .push([(0, w/2), (0, -w/2)])
    .rect(sw, sd*2, mode='s')
    # Cut left and right slots
    .push([(w/2, 0), (-w/2, 0)])
    .rect(sd*2, sw, mode='s')
    # Cut center hole
    .circle(hd/2, mode='s')
)

# 1. Vertical beam (along Z axis)
# Starts from below origin (-len_z_down) and extends upwards
beam_z = (
    cq.Workplane("XY")
    .workplane(offset=-len_z_down)
    .placeSketch(extrusion_sketch)
    .extrude(len_z_up + len_z_down)
)

# 2. Horizontal arm (along X axis)
# Standard YZ plane normal is +X
beam_x = (
    cq.Workplane("YZ")
    .placeSketch(extrusion_sketch)
    .extrude(len_x)
)

# 3. Horizontal arm (along Y axis)
# Standard XZ plane normal is +Y
beam_y = (
    cq.Workplane("XZ")
    .placeSketch(extrusion_sketch)
    .extrude(len_y)
)

# Combine all parts into a single solid object
result = beam_z.union(beam_x).union(beam_y)