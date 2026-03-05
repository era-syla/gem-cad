import cadquery as cq

# --- Dimensions and Parameters ---
length = 100.0      # Total length of the main plate
width = 30.0        # Width of the main plate
thickness = 3.0     # Thickness of the plate

pin_diam = 4.0      # Diameter of the pin on the right
pin_len = 15.0      # Length of the pin

hinge_od = 8.0      # Outer diameter of the hinge knuckle
hinge_id = 4.0      # Inner diameter (bore) of the hinge knuckle
hinge_width = 22.0  # Width of the narrow tab for the hinge
notch_len = 2.0     # Length of the cut/notch into the plate

# --- Modeling ---

# 1. Main Body: Create the base plate centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Hinge Notches: Cut the corners at the left end (-X)
# Calculate the width of the cutout on each side
cutout_width = (width - hinge_width) / 2.0

# Define a box to use as a cutting tool for the corners
# We position these boxes at the corners of the left face (x = -length/2)
# The box dimensions are doubled in the offset direction to ensure complete coverage of the corner
notch_tool_top = (
    cq.Workplane("XY")
    .box(notch_len * 2, cutout_width * 2, thickness * 2)
    .translate((-length/2, width/2, 0))
)

notch_tool_bottom = (
    cq.Workplane("XY")
    .box(notch_len * 2, cutout_width * 2, thickness * 2)
    .translate((-length/2, -width/2, 0))
)

# Apply the cuts to the main body
result = result.cut(notch_tool_top).cut(notch_tool_bottom)

# 3. Hinge Knuckle: Add the cylindrical feature at the left end
# Calculate vertical position: Top of cylinder aligned with top of plate
# Plate top is at Z = thickness/2
# Cylinder top is at Z = z_center + hinge_od/2
z_center = (thickness / 2.0) - (hinge_od / 2.0)

# Create the hollow cylinder
# Extruding with 'both=True' from the XZ plane creates the cylinder along the Y axis
knuckle = (
    cq.Workplane("XZ")
    .center(-length / 2.0, z_center)  # Axis at left edge of plate, offset vertically
    .circle(hinge_od / 2.0)           # Outer profile
    .circle(hinge_id / 2.0)           # Inner profile (creates a tube)
    .extrude(hinge_width / 2.0, both=True)
)

result = result.union(knuckle)

# 4. Pin: Add the pin to the right end (+X face)
result = (
    result.faces(">X")          # Select the rightmost face
    .workplane()                # Create a workplane on this face
    .circle(pin_diam / 2.0)     # Draw the pin profile
    .extrude(pin_len)           # Extrude outwards
)