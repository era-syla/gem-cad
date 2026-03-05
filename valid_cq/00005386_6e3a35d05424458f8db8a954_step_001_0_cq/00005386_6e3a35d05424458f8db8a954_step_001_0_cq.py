import cadquery as cq

# --- Parameters ---
# Main bracket dimensions
base_width = 50.0
base_length_rect = 20.0  # Length of the rectangular part of the base
base_length_taper = 30.0 # Length of the tapered part of the base
base_thickness = 3.0

wall_height = 40.0
wall_thickness = 3.0
chamfer_size = 10.0      # Top corners of the vertical wall

# Gusset (support rib) dimensions
gusset_width = 3.0
gusset_length = 10.0
gusset_height = 25.0
gusset_chamfer = 5.0

# GoPro-style mount dimensions
mount_y_offset = 25.0    # Height from base to center of pivot
mount_z_offset = 5.0     # Protrusion from wall
lug_thickness = 3.0
lug_gap = 3.0
lug_radius = 7.5
hole_diameter = 5.0
total_mount_width = (3 * lug_thickness) + (2 * lug_gap)

# Bottom Boss/Hole dimensions
boss_diameter = 15.0
boss_height = 5.0
center_hole_diameter = 6.5
locking_pin_hole_dia = 3.0

# --- Modeling ---

# 1. Base Plate
# Create the base shape: a rectangle that tapers to a rounded end
pts = [
    (-base_width/2, 0),
    (base_width/2, 0),
    (base_width/2, base_length_rect),
    (10.0, base_length_rect + base_length_taper), # Tapering in
    (-10.0, base_length_rect + base_length_taper),
    (-base_width/2, base_length_rect)
]

base = (cq.Workplane("XY")
        .polyline(pts)
        .close()
        .extrude(base_thickness)
        .edges("|Z and >Y") # Select the vertical edge at the very front
        .fillet(10.0)       # Round off the tip
       )

# 2. Vertical Wall
# Draw on the back face (XZ plane essentially, relative to origin)
wall = (cq.Workplane("XZ")
        .workplane(offset=-wall_thickness/2) # Center it on the X axis, offset half thickness
        .moveTo(-base_width/2, 0)
        .lineTo(base_width/2, 0)
        .lineTo(base_width/2, wall_height - chamfer_size)
        .lineTo(base_width/2 - chamfer_size, wall_height)
        .lineTo(-base_width/2 + chamfer_size, wall_height)
        .lineTo(-base_width/2, wall_height - chamfer_size)
        .close()
        .extrude(wall_thickness)
       )
# Move wall to sit on top of base and align with back edge
wall = wall.translate((0, wall_thickness/2, base_thickness))

# 3. Side Gussets (Ribs)
def create_gusset():
    g = (cq.Workplane("YZ")
         .moveTo(0, 0)
         .lineTo(gusset_length, 0)
         .lineTo(gusset_length, gusset_height - gusset_chamfer)
         .lineTo(gusset_length - gusset_chamfer, gusset_height) # Simple chamfer top
         .lineTo(0, gusset_height)
         .close()
         .extrude(gusset_width)
        )
    return g

# Create left and right gussets
gusset_l = create_gusset().translate((-base_width/2, wall_thickness, base_thickness))
gusset_r = create_gusset().translate((base_width/2 - gusset_width, wall_thickness, base_thickness))


# 4. GoPro Mount Lugs
# We need 3 lugs.
def create_lug():
    l = (cq.Workplane("YZ")
         .circle(lug_radius)
         .extrude(lug_thickness)
         )
    # Cut the hole
    l = l.faces(">X").workplane().circle(hole_diameter/2).cutThruAll()
    # Add the rectangular connection to the wall
    rect_part = (cq.Workplane("YZ")
                 .center(0, -lug_radius/2)
                 .rect(lug_radius*2, lug_radius)
                 .extrude(lug_thickness)
                 )
    # Shift rect part to align with circle center properly
    rect_part = rect_part.translate((0, lug_radius/2, 0))
    return l.union(rect_part)

# Generate the 3 lugs
lugs = cq.Workplane()
start_x = -total_mount_width / 2

for i in range(3):
    x_pos = start_x + i * (lug_thickness + lug_gap)
    # Create lug geometry
    # Draw sketch on YZ plane
    lug_sketch = (cq.Workplane("YZ")
                  .workplane(offset=x_pos)
                  .moveTo(0, 0)
                  .lineTo(mount_z_offset + lug_radius, 0) # Bottom line
                  .threePointArc((mount_z_offset + lug_radius*2, lug_radius), (mount_z_offset + lug_radius, lug_radius*2)) # Outer curve
                  .lineTo(0, lug_radius*2) # Top line back to wall
                  .close()
                  .extrude(lug_thickness)
                 )
    
    # Cut hole
    lug_sketch = (lug_sketch
                  .faces(">X")
                  .workplane()
                  .center(mount_z_offset + lug_radius, lug_radius)
                  .circle(hole_diameter/2)
                  .cutThruAll()
                  )
    
    if i == 0:
        lugs = lug_sketch
    else:
        lugs = lugs.union(lug_sketch)

# Position the lugs on the wall
lugs = lugs.translate((0, wall_thickness, base_thickness + mount_y_offset - lug_radius))


# 5. Bottom Boss
# Position: Near the rounded end of the base
boss_center_y = base_length_rect + base_length_taper - 5.0 # Approximate from visual
boss = (cq.Workplane("XY")
        .workplane(offset=-boss_height) # Start below Z=0
        .circle(boss_diameter/2)
        .extrude(boss_height)
       )
# Align boss Y
boss = boss.translate((0, boss_center_y, 0))

# Combine everything
result = base.union(wall).union(gusset_l).union(gusset_r).union(lugs).union(boss)

# 6. Cuts (Hole through base and boss, and locking pin hole)
# Vertical hole
result = (result
          .faces(">Z")
          .workplane()
          .moveTo(0, boss_center_y)
          .circle(center_hole_diameter/2)
          .cutThruAll()
         )

# Side locking pin hole in the boss
result = (result
          .faces(">Y") # Select front face
          .workplane() 
          .moveTo(0, -boss_height/2) # Move down into the boss area
          .circle(locking_pin_hole_dia/2)
          .cutThruAll() # Cut through the boss
         )

# Apply fillets to vertical edges of wall for cleaner look (optional but matches style)
# Finding vertical edges on the main wall
result = result.edges("|Z").filter(lambda e: e.Center().y < wall_thickness + 1 and e.Center().z > base_thickness).fillet(0.5)

# Fillet the base plate edges
result = result.edges("|Z").filter(lambda e: e.Center().z < base_thickness).fillet(0.5)