import cadquery as cq

# --- Parameters ---
# Overall Dimensions
main_radius = 3.5
pin_radius = 2.0
pin_height = 6.0
base_height = 25.0
shaft_height = 65.0

# Tip Dimensions
cone_height = 10.0
tip_radius = 0.5
tip_extension = 1.5

# Clip Dimensions
clip_length = 20.0
clip_width = 3.0
clip_thickness = 2.5  # Protrusion from the surface
clip_bottom_offset = 2.0  # Distance from the bottom of the base section

# --- Modeling ---

# 1. Create the bottom connection pin
# Start from the origin
result = cq.Workplane("XY").circle(pin_radius).extrude(pin_height)

# 2. Create the base section (lower cylindrical body)
# Extrude from the top of the pin
result = result.faces(">Z").workplane().circle(main_radius).extrude(base_height)

# 3. Create the side clip
# The clip is attached to the base section. We create a box positioned on the side.
# Overlap ensures a clean boolean union with the main body.
overlap = 0.5
clip_x_pos = main_radius - overlap
clip_z_pos = pin_height + clip_bottom_offset

# Create the clip geometry
clip = (cq.Workplane("XY")
        .workplane(offset=clip_z_pos)
        .moveTo(clip_x_pos, 0)
        .box(clip_thickness + overlap, clip_width, clip_length, 
             centered=(False, True, False))) 
        # centered=(X:False (grow +X), Y:True (center on axis), Z:False (grow +Z))

# Union the clip to the main body
result = result.union(clip)

# 4. Create the main shaft
# Extrude from the top of the base section. 
# A separate extrusion creates the visible seam line between base and shaft.
result = result.faces(">Z").workplane().circle(main_radius).extrude(shaft_height)

# 5. Create the conical tip
# Loft from the main radius to the small tip radius
result = (result.faces(">Z").workplane()
          .circle(main_radius)
          .workplane(offset=cone_height)
          .circle(tip_radius)
          .loft(combine=True))

# 6. Create the final probe point
# Small extrusion at the very tip
result = result.faces(">Z").workplane().circle(tip_radius).extrude(tip_extension)