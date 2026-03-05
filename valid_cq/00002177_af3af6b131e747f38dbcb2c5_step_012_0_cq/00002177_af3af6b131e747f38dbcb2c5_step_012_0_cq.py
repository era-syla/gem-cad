import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_length = 60.0
body_width = 20.0
body_height = 20.0
fillet_radius = 2.0  # Radius for the main body edges

# Side recess (label area) dimensions
recess_depth = 0.5
recess_margin = 3.0  # Distance from the edge of the face to the recess

# End cap/detail dimensions
end_detail_margin = 4.0
end_detail_depth = 0.5

# Wire dimensions
wire_diameter = 1.5
wire_length_straight = 5.0
wire_length_bend = 5.0
wire_bend_radius = 3.0
wire_spacing = 4.0

# --- Modeling ---

# 1. Create the Main Body
# Start with a box centered at origin
main_body = cq.Workplane("XY").box(body_length, body_width, body_height)

# Apply fillets to the long edges (along X axis)
# Selecting edges parallel to X
main_body = main_body.edges("|X").fillet(fillet_radius)

# 2. Create the Side Recess
# We select the front face (which is roughly +Y or -Y depending on orientation, let's assume +Y)
# We need to orient correctly. Let's pick the face with normal closest to Y.
recess_sketch = (
    main_body.faces(">Y").workplane()
    .rect(body_length - 2 * recess_margin, body_height - 2 * recess_margin)
)
main_body = recess_sketch.cutBlind(-recess_depth)

# 3. Create the End Detail (Oval/Rounded Rect on the -X face)
end_face = main_body.faces("<X").workplane()
# Create an ellipse or slot shape
end_detail = (
    end_face
    .ellipse(body_width/2 - end_detail_margin, body_height/2 - end_detail_margin)
    .cutBlind(-end_detail_depth)
)
result = end_detail

# 4. Create the Wires
# The wires come out of the +X face.
# There are three wires.
wire_face_center = result.faces(">X").val().Center()

wires = []

# Define wire offsets (Y positions relative to center)
y_offsets = [0, -wire_spacing, wire_spacing] 

for y_off in y_offsets:
    # Path for the wire: Straight out, then bend up/down/straight
    # Let's make them S-shaped or just bent for realism
    
    # Start point on the face
    p0 = (body_length / 2, y_off, 0)
    
    # Define a path using a spline for a natural wire look
    # Point 1: slightly out in X
    p1 = (body_length / 2 + 3, y_off, 0)
    # Point 2: further out and bending slightly in Z or Y. Let's bend them randomly or uniform.
    # The image shows them curving upwards/outwards.
    p2 = (body_length / 2 + 8, y_off + (1 if y_off == 0 else y_off*0.5), 2)
    p3 = (body_length / 2 + 15, y_off + (2 if y_off == 0 else y_off*0.8), 4)

    path = cq.Workplane("XY").moveTo(p0[0], p0[1]).lineTo(p1[0], p1[1]).spline([p2, p3], includeCurrent=True)
    
    # Create the wire cross-section
    wire = (
        cq.Workplane("YZ")
        .workplane(offset=body_length / 2)
        .center(y_off, 0)
        .circle(wire_diameter / 2)
        .sweep(path)
    )
    wires.append(wire)

# Combine wires with the main body
for w in wires:
    result = result.union(w)

# Assign to final variable
result = result