import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------

# Central Pin Dimensions
pin_diameter = 6.0
pin_length = 24.0

# Wing Dimensions
wing_width = 16.0       # Major axis length of the elliptical profile
wing_thickness = 8.0    # Minor axis length of the elliptical profile
wing_depth = 18.0       # Length of the wing extrusion along the pin axis
wing_angle = 15.0       # Dihedral angle (degrees) upwards from horizontal
wing_overlap = 1.0      # Overlap between wing and pin for solid union
wing_fillet = 1.2       # Fillet radius for the wing edges

# -----------------------------------------------------------------------------
# Modeling
# -----------------------------------------------------------------------------

# 1. Create the Central Pin
# Oriented along the Y axis, centered at the origin
pin = (
    cq.Workplane("XZ")
    .circle(pin_diameter / 2.0)
    .extrude(pin_length / 2.0, both=True)
)

# Apply a fillet to the ends of the pin to create the rounded capsule look.
# We use slightly less than the radius to avoid geometric singularities at the pole.
pin = pin.edges("<Y or >Y").fillet(pin_diameter / 2.0 - 0.05)


# 2. Create the Wing Geometry
# We create a generic wing centered at the origin first.
# The profile is an ellipse on the XZ plane.
wing_profile = (
    cq.Workplane("XZ")
    .ellipse(wing_width / 2.0, wing_thickness / 2.0)
)

# Extrude the profile along Y
wing_solid = wing_profile.extrude(wing_depth / 2.0, both=True)

# Apply fillets to the edges of the wing end faces.
# Since the side of the extrusion is smooth, edges() selects the top and bottom loops.
wing_solid = wing_solid.edges().fillet(wing_fillet)


# 3. Position the Right Wing
# Calculate the X shift to position the wing tangent/overlapping the pin
# Shift = Pin Radius + Wing Radius - Overlap
x_shift = (pin_diameter / 2.0) + (wing_width / 2.0) - wing_overlap

right_wing = wing_solid.translate((x_shift, 0, 0))

# Rotate the wing upwards (around the Y axis) to achieve the butterfly shape
right_wing = right_wing.rotate((0, 0, 0), (0, 1, 0), wing_angle)


# 4. Create the Left Wing
# Mirror the right wing across the YZ plane
left_wing = right_wing.mirror("YZ")


# 5. Combine Components
# Union the pin and both wings into a single solid
result = pin.union(right_wing).union(left_wing)

# -----------------------------------------------------------------------------
# The 'result' variable now contains the final CadQuery object
# -----------------------------------------------------------------------------