import cadquery as cq

# --- Parametric Dimensions ---
# Based on typical NEMA 17 bracket dimensions and visual estimation
bracket_width = 80.0
bracket_height = 42.0  # Approx standard size
thickness = 6.0

# Central Bore
center_bore_diameter = 22.0
keyway_width = 3.0
keyway_depth = 1.5  # From bore surface

# Mounting Holes (Outer frame)
outer_hole_spacing_x = 70.0 # Wide spacing for table mounting
outer_hole_spacing_y = 20.0 # Vertical spacing
outer_hole_diameter = 4.0

# Motor Mounting Holes (Inner)
# NEMA 17 standard is usually 31mm spacing
motor_mount_spacing = 31.0 
motor_mount_hole_dia = 3.5

# Shape construction parameters
top_flat_width = 80.0
top_flat_height = 10.0 # The rectangular bar at the top
corner_radius = 4.0

# --- Geometry Construction ---

# 1. Create the main silhouette
# We'll sketch on the XY plane.
# The shape is roughly trapezoidal with a rectangular bar on top.

# Calculate points for the polygon outline
# Bottom width is narrower than top bar
bottom_width = 50.0 
height_overall = 50.0

# Let's try a different approach: Union of primitive shapes might be messy. 
# A sketch is cleaner.
# Center of the motor hole will be at (0,0)

motor_center_y = 0.0
top_edge_y = 25.0
bottom_edge_y = -25.0

# Let's build the main profile
# Top Bar
pts_top_bar = [
    (-bracket_width/2, top_edge_y),
    (bracket_width/2, top_edge_y),
    (bracket_width/2, top_edge_y - top_flat_height),
    (-bracket_width/2, top_edge_y - top_flat_height)
]

# The trapezoidal/triangular body
# It connects to the top bar and goes down.
# Let's model it as a custom polygon.

# Points definition (Counter-Clockwise)
p1 = (-bracket_width/2, top_edge_y) # Top Left
p2 = (bracket_width/2, top_edge_y)  # Top Right
p3 = (bracket_width/2, top_edge_y - top_flat_height) # Top Right lower corner
p4 = (45.0/2, -18.0) # Bottom Right Corner (approx)
p5 = (-45.0/2, -18.0) # Bottom Left Corner (approx)
p6 = (-bracket_width/2, top_edge_y - top_flat_height) # Top Left lower corner

# Wait, the image shows a specific shape. 
# Let's refine the points based on a typical "flat" stepper bracket.
# It looks like a standard NEMA 17 mount plate.
# The top is a straight bar. The bottom is angled inwards.

width = 85.0
height = 50.0
thickness = 6.0
center_y = -5.0 # Shift the motor mount down relative to the top bar

# Constructing with a sketch
sketch = (
    cq.Workplane("XY")
    .moveTo(-width/2, height/2)
    .lineTo(width/2, height/2)
    .lineTo(width/2, height/2 - 12) # Top side thickness
    .lineTo(30, -height/2 + 8)      # Angle down to bottom right
    .lineTo(30, -height/2)          # Vertical small edge
    .lineTo(-30, -height/2)         # Bottom flat
    .lineTo(-30, -height/2 + 8)     # Vertical small edge
    .lineTo(-width/2, height/2 - 12) # Angle up to top left
    .close()
)

# Extrude the base shape
base = sketch.extrude(thickness)

# Add fillets to the corners
# We select edges perpendicular to Z plane (vertical edges in 2D view)
base = base.edges("|Z").fillet(2.0)

# --- Features ---

# 1. Central Hole with Keyway/Notch
# The notch is at the top of the hole in the image.
motor_center = (0, center_y)

base = (
    base.faces(">Z").workplane()
    .center(*motor_center)
    .circle(center_bore_diameter/2)
    .cutThruAll()
)

# Add the notch
notch_width = 4.0
notch_height = 4.0 # Height into the material from the hole edge
radius = center_bore_diameter / 2

base = (
    base.faces(">Z").workplane()
    .center(*motor_center)
    .moveTo(-notch_width/2, radius - 1.0)
    .lineTo(notch_width/2, radius - 1.0)
    .lineTo(notch_width/2, radius + notch_height)
    .lineTo(-notch_width/2, radius + notch_height)
    .close()
    .cutThruAll()
)


# 2. Mounting Holes (Top Bar)
# Two holes on the far ends of the top bar
top_hole_spacing = width - 12.0 # 6mm from edges
top_hole_y = height/2 - 6.0
top_hole_dia = 5.0

base = (
    base.faces(">Z").workplane()
    .pushPoints([(-top_hole_spacing/2, top_hole_y), (top_hole_spacing/2, top_hole_y)])
    .hole(top_hole_dia)
)

# 3. Motor Mounting Holes
# The image shows 4 holes arranged around the central bore.
# However, the bottom two are clearly visible on the lower flange.
# The top two seem to be integrated or close to the top bar structure.
# Looking closely at the image, there are holes on the "wings" (angled part)
# and holes on the bottom flat part.

# Let's interpret the holes from the image specifically:
# - Two large holes on the very top ears (already done)
# - Two holes on the angled sides (mid-way down)
# - Two holes on the bottom flat section.

# Actually, re-evaluating the image:
# It looks like a standard NEMA 17 face plate pattern (31mm square) PLUS outer mounting holes.
# The four holes around the big center hole are the motor mounts.
# The two holes at the far top corners are for mounting the bracket to something else.
# The two holes at the bottom corners are also for mounting the bracket.

# Let's punch the NEMA 17 pattern (31mm x 31mm) centered on the big hole
nema_hole_spacing = 31.0
nema_hole_dia = 3.5

# We need to be careful because the top two NEMA holes might cut into the fillet area
# or the solid part of the bracket.
# In the image, we see two holes clearly below the center line (on the legs).
# We see two holes clearly above the center line (near the top bar junction).
# This creates the 4-bolt pattern.

base = (
    base.faces(">Z").workplane()
    .center(*motor_center)
    .rect(nema_hole_spacing, nema_hole_spacing, forConstruction=True)
    .vertices()
    .hole(nema_hole_dia)
)

# 4. Additional Outer Mounting Holes
# The image shows holes at the very bottom corners as well.
bottom_hole_spacing = 50.0 # Distance between bottom holes
bottom_hole_y = -height/2 + 5.0
bottom_hole_dia = 4.0

# To correctly place these relative to the global origin (which was center of sketch bounding box)
# We need to move relative to the center_y used for the motor.
# The bottom edge is at y = -height/2.

base = (
    base.faces(">Z").workplane()
    # Reset origin to global (0,0) of the workplane
    .pushPoints([(-bottom_hole_spacing/2, bottom_hole_y), (bottom_hole_spacing/2, bottom_hole_y)])
    .hole(bottom_hole_dia)
)

# 5. Countersinking/Counterboring (Optional based on visual, but image looks like plain holes)
# The image has sharp edges, standard CAD look.

# Final cleanup - Fillet the outer corners specifically if the generic fillet missed intended aesthetic
# The code applied a generic Z-parallel fillet earlier which handles the main shape.

result = base