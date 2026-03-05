import cadquery as cq

# --- Parameter Definitions ---
# Base dimensions
base_dia = 40.0
base_height = 3.0
base_chamfer = 1.0

# Mounting holes
hole_pattern_radius = 14.0
hole_dia = 3.2
num_holes = 3

# GoPro-style Mount dimensions
mount_width = 15.0      # Total width along the pin axis
mount_depth = 15.0      # Thickness/Depth (front to back)
mount_height = 18.0     # Height from top of base
prong_gap = 3.6         # Gap between prongs
mount_hole_dia = 5.0    # Cross hole diameter

# Connector Block dimensions
block_width = 12.0
block_height = 12.0
block_length_extension = 18.0 # From center to where pin starts

# Pin dimensions
pin_dia = 6.0
pin_len = 22.0

# --- Geometry Construction ---

# 1. Base Plate
# Create the disk and add a chamfer to the top edge for the rim effect
base = (cq.Workplane("XY")
        .circle(base_dia / 2.0)
        .extrude(base_height)
        .edges(">Z")
        .chamfer(base_chamfer))

# Cut the mounting holes
base = (base.faces(">Z")
        .workplane()
        .polarArray(hole_pattern_radius, 0, 360, num_holes)
        .circle(hole_dia / 2.0)
        .cutThruAll())

# 2. Connector Block
# A square beam extending from the center out to the side (-X direction)
# Positioned to sit on top of the base
connector = (cq.Workplane("YZ")
             .workplane(offset=-block_length_extension) # Start plane at end of block
             .moveTo(0, base_height + block_height/2.0)
             .rect(block_width, block_height)
             .extrude(block_length_extension)) # Extrude back to center

# 3. Mount Tower (The prongs)
# Centered on the base
mount_tower = (cq.Workplane("XY")
               .workplane(offset=base_height)
               .rect(mount_depth, mount_width)
               .extrude(mount_height))

# Round off the top of the tower
# We filter for edges at the top that are parallel to Y axis (width)
mount_tower = mount_tower.edges(">Z and |Y").fillet(mount_depth / 2.0 - 0.01)

# Cut the cross hole for the mount
# Calculated Z height for the hole center relative to the workplane
hole_z_center = base_height + mount_height - (mount_depth / 2.0)

mount_tower = (mount_tower.faces(">Y")
               .workplane(centerOption="ProjectedOrigin")
               .moveTo(0, hole_z_center)
               .circle(mount_hole_dia / 2.0)
               .cutThruAll())

# Cut the gap to create the two prongs
mount_tower = (mount_tower.faces(">Z")
               .workplane()
               .rect(mount_depth * 2, prong_gap) # Width exaggerated to ensure cut
               .cutThruAll())

# 4. Side Pin
# Extruding from the face of the connector block
pin = (connector.faces("<X")
       .workplane()
       .center(0, 0) # Center on the face
       .circle(pin_dia / 2.0)
       .extrude(pin_len))

# Chamfer the tip of the pin
pin = pin.edges("<X").chamfer(0.5)

# --- Combine All Parts ---
result = base.union(mount_tower).union(connector).union(pin)

# Optional: Fillet the junction where the connector meets the base/mount for smoothness
# result = result.edges("(>Z[0] and >X[-10] and <X[0])").fillet(1.0) # Complex selector omitted for stability