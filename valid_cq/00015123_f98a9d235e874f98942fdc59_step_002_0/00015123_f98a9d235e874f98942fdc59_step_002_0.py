import cadquery as cq

# --- Parameters ---
# Main Hub Ring
hub_od = 45.0
hub_id = 30.0
hub_width = 16.0

# Vertical Arm (Stem)
arm_height = 75.0        # Center of hub to base of clevis
arm_base_width_x = 16.0  # Matches hub width
arm_base_width_y = 20.0  # Slightly wider at the base to blend with hub
arm_top_width = 14.0     # Square profile at top
arm_top_thick = 14.0

# Clevis (Fork)
clevis_height = 22.0
clevis_slot_width = 6.0
clevis_pin_diameter = 6.0
clevis_fillet_radius = 2.0

# Side Mounting Boss
boss_y_offset = 26.0     # Distance from center
boss_width_x = 16.0
boss_len_y = 14.0
boss_height_z = 12.0
boss_hole_diameter = 5.0

# Bottom Feature
bottom_boss_size = 12.0
bottom_hole_diameter = 5.0

# --- Geometry Construction ---

# 1. Create the Main Hub (Ring)
# Aligned along the X-axis
hub = (cq.Workplane("YZ")
       .circle(hub_od / 2.0)
       .extrude(hub_width)
       .translate((-hub_width / 2.0, 0, 0)) # Center the hub on X=0
       )

# Cut the main bore
hub = hub.faces("<X").workplane().hole(hub_id)


# 2. Create the Tapered Arm
# We use a loft operation from a rectangle just above the hub to the top.
# Start the loft slightly inside the hub to ensure a solid overlap.
loft_start_z = (hub_od / 2.0) - 2.0
loft_end_z = arm_height

# Define base profile
arm_base = (cq.Workplane("XY")
            .workplane(offset=loft_start_z)
            .rect(arm_base_width_x, arm_base_width_y)
           )

# Define top profile
arm_top_plane = cq.Workplane("XY").workplane(offset=loft_end_z)
# Construct the loft (create solid)
arm = arm_base.workplane(offset=loft_end_z - loft_start_z).rect(arm_top_width, arm_top_thick).loft(combine=False)


# 3. Create the Clevis (Fork)
# Build a block on top of the arm
clevis_block = (cq.Workplane("XY")
                .workplane(offset=loft_end_z)
                .rect(arm_top_width, arm_top_thick)
                .extrude(clevis_height)
                )

# Fillet the top edges to create the rounded ears
# The pin is parallel to X, so the "ears" are in the YZ plane profile.
# We fillet the edges running along Y at the top.
clevis_block = clevis_block.edges("|Y and >Z").fillet(arm_top_thick / 2.0 - 0.01)

# Cut the Slot
# Slot cuts through the middle of the X-width
clevis_block = (clevis_block.faces(">Z").workplane()
                .rect(clevis_slot_width, arm_top_thick * 2) # Length acts as infinite cut in Y
                .cutBlind(-(clevis_height - 6.0)) # Depth of slot
                )

# Cut the Pin Hole
# Hole goes through X-axis, centered on the rounded top part
# Calculate center offset relative to the face center
face_center_z = loft_end_z + (clevis_height / 2.0)
target_hole_z = loft_end_z + clevis_height - (arm_top_thick / 2.0)
offset_z = target_hole_z - face_center_z

clevis_block = (clevis_block.faces(">X").workplane()
                .center(0, offset_z)
                .hole(clevis_pin_diameter)
                )


# 4. Create the Side Boss
# Located on the +Y side
boss = (cq.Workplane("XY")
        .workplane(offset=-boss_height_z / 2.0 + 2.0) # Position vertically relative to hub center
        .center(0, boss_y_offset)
        .rect(boss_width_x, boss_len_y)
        .extrude(boss_height_z)
        )

# Round the outer corners of the boss
boss = boss.edges("|Z").fillet(3.0)

# Add the mounting hole
boss = boss.faces(">Z").workplane().hole(boss_hole_diameter)


# 5. Create Bottom Feature
# Small protrusion at the bottom of the ring
bottom_feat = (cq.Workplane("XY")
               .workplane(offset=-(hub_od / 2.0) + 1.0)
               .rect(bottom_boss_size, bottom_boss_size)
               .extrude(-4.0)
               )
# Radial hole at bottom
bottom_feat = bottom_feat.faces("<Z").workplane().hole(bottom_hole_diameter)


# --- Assembly and Refinement ---

# Union all components
result = hub.union(arm).union(clevis_block).union(boss).union(bottom_feat)

# Apply fillets to smooth transitions (Casting look)
# Neck transition (Arm to Hub)
try:
    result = result.edges(cq.selectors.BoxSelector(
        (-10, -10, hub_od/2 - 5), 
        (10, 10, hub_od/2 + 5)
    )).fillet(3.0)
except:
    pass

# Boss transition (Boss to Hub)
try:
    # Select edges near the intersection of boss and hub
    result = result.edges(cq.selectors.NearestToPointSelector((0, hub_od/2, 0))).fillet(2.0)
except:
    pass
