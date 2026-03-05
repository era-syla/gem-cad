import cadquery as cq

# --- Parameter Definitions ---
height = 140.0         # Total height of the model
tube_od = 20.0         # Outer diameter of the main tube
tube_id = 16.0         # Inner diameter (hollow core)
sleeve_od = 23.0       # Outer diameter of the bottom reinforced section
sleeve_height = 40.0   # Height of the bottom section

# Fin dimensions
fin_height = 70.0      # Vertical length of the fin
fin_width = 30.0       # Horizontal width at the bottom
fin_thickness = 2.0    # Thickness of the fin plate
num_fins = 3           # Number of fins

# Top detail dimensions
notch_depth = 15.0     # Depth of the V-cut
notch_width = 14.0     # Width of the V-cut at the rim
tab_width = 8.0        # Width of the protruding tab
tab_protrusion = 8.0   # How far the tab sticks out from the tube
tab_height = 12.0      # Vertical height of the tab

# --- Modeling ---

# 1. Create the Main Body
# Main vertical tube
main_tube = cq.Workplane("XY").circle(tube_od / 2.0).extrude(height)

# Bottom reinforced sleeve (slightly larger diameter)
sleeve = cq.Workplane("XY").circle(sleeve_od / 2.0).extrude(sleeve_height)

# Union the tube and sleeve
body = main_tube.union(sleeve)

# Hollow out the center to create a pipe
bore = cq.Workplane("XY").circle(tube_id / 2.0).extrude(height)
body = body.cut(bore)

# 2. Create the Fins
# We define a single fin on the XZ plane.
# The shape is a right triangle with the vertical edge along the tube.
# We embed the root slightly into the tube to ensure a solid union.
fin_root_x = tube_od / 2.0 - 0.5 

fin_sketch = (
    cq.Workplane("XZ")
    .polyline([
        (fin_root_x, 0),                 # Bottom inner point
        (fin_root_x + fin_width, 0),     # Bottom outer point
        (fin_root_x, fin_height)         # Top inner point
    ])
    .close()
    .extrude(fin_thickness / 2.0, both=True) # Extrude symmetrically to create thickness
)

# Replicate fins radially
fins = fin_sketch
for i in range(1, num_fins):
    angle = i * (360.0 / num_fins)
    rot_fin = fin_sketch.rotate((0, 0, 0), (0, 0, 1), angle)
    fins = fins.union(rot_fin)

body = body.union(fins)

# 3. Create Top Features (Notch and Tab)
# We align the Notch to the "Front" (-Y direction) and the Tab to the "Back" (+Y direction).

# V-Notch Cut
# Draw V shape on XZ plane at the top. 
# Workplane("XZ") normal points to -Y. Extruding positive values goes in -Y direction.
# This conveniently cuts the front face of the tube without touching the back face.
notch_cutter = (
    cq.Workplane("XZ")
    .moveTo(0, height)
    .lineTo(notch_width / 2.0, height)
    .lineTo(0, height - notch_depth)
    .lineTo(-notch_width / 2.0, height)
    .close()
    .extrude(tube_od) # Extrude deep enough to cut the front wall
)
body = body.cut(notch_cutter)

# Tab (Launch Lug/Hook)
# Create a rectangular block on the back side (+Y).
# Positioned at the top rim.
tab_y_pos = tube_od / 2.0 + tab_protrusion / 2.0 - 1.0 # -1.0 overlap ensures connection
tab = (
    cq.Workplane("XY")
    .workplane(offset=height - tab_height)
    .center(0, tab_y_pos)
    .rect(tab_width, tab_protrusion)
    .extrude(tab_height)
)
body = body.union(tab)

# --- Final Result ---
result = body