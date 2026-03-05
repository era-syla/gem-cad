import cadquery as cq

# Parametric dimensions
wheel_radius = 35.0
wheel_thickness = 16.0
wheel_base = 140.0
frame_thickness = 12.0
handlebar_length = 60.0
handlebar_radius = 3.0

# Define the 2D profile sketch for the bicycle frame
# Using overlapping rectangular segments to form the continuous frame body
frame_sketch = (
    cq.Sketch()
    # Beam 1 (Chainstay / lower body): Rear axle to bottom bracket
    .push([(30, 5)])
    .rect(65, 20, angle=9.46)
    # Beam 2 (Downtube / main body): Bottom bracket to headset
    .push([(85, 35)])
    .rect(75, 20, angle=45.0)
    # Front Fork: Headset to front axle
    .push([(125, 30)])
    .rect(72, 16, angle=-63.43)
    # Seatpost: Extending from the main body
    .push([(60, 45)])
    .rect(55, 12, angle=126.87)
    # Bottom Bracket (Crank area bulge)
    .push([(60, 10)])
    .circle(16)
    # Seat
    .push([(43, 65)])
    .rect(35, 8, angle=10.0)
    # Stem (connecting frame to handlebar)
    .push([(112.5, 67.5)])
    .rect(20, 12, angle=71.57)
    .clean()
)

# Create 3D frame by extruding the sketch symmetrically
frame = (
    cq.Workplane("XZ")
    .placeSketch(frame_sketch)
    .extrude(frame_thickness / 2.0, both=True)
)

# Create the front and rear wheels
wheels = (
    cq.Workplane("XZ")
    .pushPoints([(0, 0), (wheel_base, 0)])
    .circle(wheel_radius)
    .extrude(wheel_thickness / 2.0, both=True)
)

# Create the handlebar
handlebar = (
    cq.Workplane("XZ")
    .center(115, 75)
    .circle(handlebar_radius)
    .extrude(handlebar_length / 2.0, both=True)
)

# Combine all components into the final geometry
result = frame.union(wheels).union(handlebar)