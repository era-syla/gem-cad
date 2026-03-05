import cadquery as cq

# --- Parameter Definitions ---
# Shaft dimensions
shaft_diam = 10.0
shaft_rad = shaft_diam / 2.0
shaft_length = 30.0

# Tip dimensions
tip_radius = shaft_rad  # Hemispherical tip

# Spline/Knurl section dimensions
spline_diam = 11.2
spline_rad = spline_diam / 2.0
spline_length = 6.0
num_splines = 24
spline_groove_rad = 0.4
spline_chamfer = 0.5

# Head dimensions
head_diam = 19.0
head_rad = head_diam / 2.0
head_thickness = 5.0
head_fillet = 2.0  # Large fillet for the rounded outer rim

# Head detail (recess/button)
recess_outer_rad = 6.5
recess_inner_rad = 5.5
recess_depth = 0.6

# --- Geometry Construction ---

# 1. Tip
# Create a sphere centered at origin.
# The section from Z < 0 will serve as the rounded tip.
# The section Z > 0 will be buried inside the shaft.
tip = cq.Workplane("XY").sphere(tip_radius)

# 2. Shaft
# Create the main cylindrical body starting from Z=0.
shaft = cq.Workplane("XY").circle(shaft_rad).extrude(shaft_length)

# 3. Spline Section
# Positioned at the end of the shaft.
# We first create a base cylinder, then chamfer the lead-in, then cut grooves.
spline_base = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(spline_rad)
    .extrude(spline_length)
    .edges("<Z").chamfer(spline_chamfer)  # Chamfer the transition from shaft to spline
)

# Create the cutting tool for the splines (longitudinal grooves)
spline_cuts = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .polarArray(spline_rad, 0, 360, num_splines)
    .circle(spline_groove_rad)
    .extrude(spline_length)
)

# Apply the cuts to the spline base
splines = spline_base.cut(spline_cuts)

# 4. Head
# Positioned after the spline section.
head_z_start = shaft_length + spline_length

# Create the basic head shape
head_base = (
    cq.Workplane("XY")
    .workplane(offset=head_z_start)
    .circle(head_rad)
    .extrude(head_thickness)
)

# Apply a large fillet to the outer top edge to create the rounded button/flange look
head_shaped = head_base.edges(">Z").fillet(head_fillet)

# Create the detail on the back face (annular groove)
# We select the top face, draw two concentric circles, and perform a cut
head_final = (
    head_shaped.faces(">Z").workplane()
    .circle(recess_outer_rad)
    .circle(recess_inner_rad)
    .cutBlind(-recess_depth)
)

# --- Final Assembly ---
# Union all components into a single solid
result = tip.union(shaft).union(splines).union(head_final)