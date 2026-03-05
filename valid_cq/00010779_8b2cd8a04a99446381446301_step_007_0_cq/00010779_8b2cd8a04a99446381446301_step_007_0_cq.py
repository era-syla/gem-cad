import cadquery as cq

# Parameters
outer_diameter = 40.0
inner_diameter = 12.0
height = 12.0
slit_width = 3.0
screw_head_diameter = 8.0
screw_body_diameter = 4.0
counterbore_depth = 5.0

# Create the main body
# 1. Start with a solid cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(height)

# 2. Cut the central shaft hole
result = result.faces(">Z").workplane().hole(inner_diameter)

# 3. Create the slit
# We create a box to subtract from the main body.
# The box needs to be positioned to cut from the edge to the center.
# The image shows the slit aligned with an axis (let's say X).
slit = (
    cq.Workplane("XY")
    .box(outer_diameter / 2 + inner_diameter/2, slit_width, height)
    .translate((- (outer_diameter / 2 + inner_diameter/2) / 2, 0, height / 2))
)
result = result.cut(slit)

# 4. Create the clamping screw hole (counterbored hole)
# The hole goes tangentially through the solid part, perpendicular to the slit.
# Looking at the image, the screw hole is on the side, likely centered vertically.
# It seems to go through one side of the "C", across the gap, and into the other side.
# Usually, one side is a clearance hole + counterbore, the other is tapped.
# For geometric modeling, a counterbored through-hole on one side and a simple hole on the other works, 
# or a single operation if simplified.
# Based on the image, we see a counterbore on the visible face.

# Let's define the position. The hole axis is along the Y-axis (perpendicular to the slit which is along X).
# It needs to be offset from the center so it passes through the solid material, not the central hole.
# Visually, it looks like it's intersecting the solid part of the ring.
screw_offset = (outer_diameter/2 + inner_diameter/2) / 2  # Just a guess, mid-wall?
# Actually, standard shaft collars have the screw tangential to the shaft hole, or passing through the split.
# This specific design looks like a split shaft collar where the screw tightens the gap.
# The screw hole axis is perpendicular to the slit plane.
# So if the slit is on the -X side (as positioned above), the screw goes along the Y axis through the "jaws".

# Let's re-orient for clarity. 
# Slit: A cut along the X-axis from the center to -X.
# Screw Hole: Drilled along the Y-axis, passing through the slit gap.
# Position X: Somewhere in the negative X region, centered in the solid wall thickness.
wall_thickness = (outer_diameter - inner_diameter) / 2
screw_x_pos = - (inner_diameter/2 + wall_thickness/2)

# Create the counterbored hole perpendicular to the slit
# We select the side face closest to us in the image (which would be along Y)
result = (
    result.faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(screw_x_pos, 0, 0)) # Shift to the correct X position relative to center
    .cboreHole(screw_body_diameter, screw_head_diameter, counterbore_depth, depth=outer_diameter)
)

# Optional: Add small fillets to the sharp edges for realism if desired, 
# but often standard CAD models are sharp. The image shows slight softening, maybe 0.5mm.
# result = result.edges().fillet(0.5) 

# For strict adherence to the request "Return ONLY the Python code", I will skip purely aesthetic fillets 
# unless they are major features, to keep the parametric logic clean. 
# The inner hole edges look chamfered or filleted slightly in the image.
result = result.faces(">Z or <Z").edges("not %Circle").fillet(0.5)

# Export or visualization would happen here, but we just need the 'result' variable.