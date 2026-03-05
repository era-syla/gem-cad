import cadquery as cq

# Parametric dimensions
plate_length = 80.0
plate_height = 40.0
plate_thickness = 10.0

hole_diameter = 8.0
hole_spacing = 40.0  # Distance between hole centers
# Holes are centered vertically
# Holes are symmetric horizontally around the center

# Create the base plate
base = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# Create the holes
# We push points to the locations of the holes and then cut them
# The holes are located along the X-axis, centered on the Y-axis
hole_locations = [(-hole_spacing / 2, 0), (hole_spacing / 2, 0)]

result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cboreHole(hole_diameter, hole_diameter * 1.8, 2.0) # Using counterbore to match the visual style, or simple hole if flat
    # Looking closely at the image, it looks like a simple countersink or just a through hole with lighting artifacts. 
    # However, standard mechanical parts like this often have countersinks. 
    # Let's stick to a simple through hole with a chamfer to be safe, or just a straight hole.
    # Re-evaluating image: It looks like a straight through hole. Let's do a simple hole.
)

# Re-creating with simple holes as the safest interpretation of the visual data
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_height, plate_thickness)
    .faces(">Y") # Choosing a face to sketch on, though box centers at origin
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)

# Actually, let's refine the orientation to match the isometric view better.
# The view shows the thickness along a diagonal.
# Let's assume Length along X, Height along Z, Thickness along Y for the initial box,
# then rotate or just build it flat on XY. 
# Building flat on XY (Length=X, Height=Y, Thickness=Z) is standard.

# Final Code Construction
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_thickness, plate_height) # Box centered at origin
    .faces(">Y") # Select the front face
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, hole_diameter * 2.0, 82.0) # Adding a countersink based on the visible rim
)

# Wait, looking at the image again very carefully.
# The hole on the right shows the inner cylinder clearly. The hole on the left shows the same.
# There is a slight bevel at the opening, indicating a countersink or chamfer.
# Let's use a standard countersink (cskHole).

# Let's adjust dimensions to be more realistic for a generic bracket.
L = 100.0
W = 50.0
T = 10.0
Hole_Dia = 10.0
Hole_Dist = 50.0

result = (
    cq.Workplane("XY")
    .box(L, W, T)
    .faces(">Z")
    .workplane()
    .pushPoints([(-Hole_Dist/2, 0), (Hole_Dist/2, 0)])
    .cskHole(Hole_Dia, Hole_Dia * 1.5, 90) # Countersink hole
)

# The image shows the plate standing up. Let's orient it so the result variable holds it in that orientation if exported,
# but usually, standard orientation (flat on Z) is preferred for CAD.
# I will stick to the flat orientation as it is standard practice, but the prompt implies "create this model", 
# often implying similar visual aspect.
# Let's build it flat.

# Refined parameters based on visual ratios:
# Length ~ 2x Height
# Thickness ~ 1/4 Height
# Hole diameter ~ 1/4 Height
# Distance between holes ~ 1/2 Length

length = 100.0
height = 50.0
thickness = 10.0
hole_diam = 12.0
csk_diam = 18.0
csk_angle = 90.0
hole_spacing = 50.0

result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .cskHole(hole_diam, csk_diam, csk_angle)
)