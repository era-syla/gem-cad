import cadquery as cq

# --- Parameter Definitions ---
# Base Block Parameters
base_width = 30.0    # Width of the rectangular base
base_depth = 20.0    # Depth of the rectangular base
base_height = 12.0   # Height of the rectangular base

# Base Hole Parameters
side_hole_diam = 4.0     # Diameter of the hole on the side face
front_hole_diam = 6.0    # Diameter of the hole on the front face (likely for a clamp/bolt)
slot_width = 2.0         # Width of the horizontal slot in the base

# Cylindrical Tower Parameters
# Level 1 (Bottom wide cylinder)
cyl1_diam = 18.0
cyl1_height = 10.0
cyl1_flange_diam = 20.0  # Thin flange at bottom
cyl1_flange_height = 1.0

# Level 2 (Middle cylinder)
cyl2_diam = 18.0
cyl2_height = 10.0
cyl2_flange_diam = 20.0  # Thin flange
cyl2_flange_height = 1.0

# Level 3 (Neck)
cyl3_diam = 12.0
cyl3_height = 8.0
cyl3_base_flange_diam = 16.0 # Flange at base of neck
cyl3_base_flange_height = 1.0

# Level 4 (Top cap)
top_cap_diam = 14.0
top_cap_height = 4.0

# Through Hole
center_hole_diam = 6.0

# --- Geometry Construction ---

# 1. Create the Base Block
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# 2. Create the Horizontal Slot in the Base
# Assuming the slot goes through the side at a specific height
slot = (cq.Workplane("YZ")
        .workplane(offset=base_width/2 + 1) # Start outside
        .moveTo(0, -base_height/4) # Approximate position
        .rect(base_depth * 2, slot_width)
        .extrude(-base_width - 2)
       )
base = base.cut(slot)

# 3. Create the Holes in the Base
# Side hole
base = base.faces(">X").workplane().moveTo(0, 0).hole(side_hole_diam)

# Front hole (centered on the split/slot usually)
base = base.faces(">Y").workplane().moveTo(0, -base_height/4).hole(front_hole_diam, depth=base_depth/2 + 5)


# 4. Construct the Vertical Tower
# We will build this stack upwards from the top of the base.
# It's offset from the center of the block based on the image.
tower_center_offset = -base_width/4 

# Define the local workplane on top of the base
tower_plane = base.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(tower_center_offset, 0)

# Bottom Flange/Ring
tower = tower_plane.circle(cyl1_flange_diam/2).extrude(cyl1_flange_height)

# First main section
tower = tower.faces(">Z").workplane().circle(cyl1_diam/2).extrude(cyl1_height)

# Middle Flange/Ring
tower = tower.faces(">Z").workplane().circle(cyl2_flange_diam/2).extrude(cyl2_flange_height)

# Second main section
tower = tower.faces(">Z").workplane().circle(cyl2_diam/2).extrude(cyl2_height)

# Neck Flange/Ring
tower = tower.faces(">Z").workplane().circle(cyl3_base_flange_diam/2).extrude(cyl3_base_flange_height)

# Neck section (narrower)
tower = tower.faces(">Z").workplane().circle(cyl3_diam/2).extrude(cyl3_height)

# Top Cap
tower = tower.faces(">Z").workplane().circle(top_cap_diam/2).extrude(top_cap_height)

# 5. Create the Central Through-Hole
# We drill from the very top face down through everything
result = tower.faces(">Z").workplane().hole(center_hole_diam)

# Optional: Add fillets to smooth edges slightly (optional based on image style, leaving sharp for CAD precision)
# result = result.edges("|Z").fillet(0.5) 

# If you are running this in a standard python script, you might want to export:
# cq.exporters.export(result, "model.step")