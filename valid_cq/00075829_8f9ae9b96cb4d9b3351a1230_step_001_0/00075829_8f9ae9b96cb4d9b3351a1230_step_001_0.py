import cadquery as cq

# --- Parametric Dimensions ---
length = 80.0             # Distance from clevis center to ball center
shaft_diameter = 6.0      # Main rod diameter
ball_diameter = 13.0      # Ball end diameter
clevis_diameter = 14.0    # Clevis head diameter
clevis_thickness = 10.0   # Total height of the clevis
slot_gap = 4.0            # Height of the slot cutout
wall_thickness = 4.0      # Thickness of material connecting shaft to clevis ears
rib_length = 10.0         # Length of the gusset rib
rib_height = 4.0          # Height of the gusset rib
flat_width = 8.0          # Length of the wrench flat section
flat_offset = 12.0        # Distance from ball center to wrench flats
flat_cut_depth = 0.5      # Depth of the wrench flat cut

# --- Geometry Construction ---

# 1. Clevis End (Head)
# Create the main cylinder for the head, centered vertically on Z=0
clevis = (
    cq.Workplane("XY")
    .circle(clevis_diameter / 2.0)
    .extrude(clevis_thickness)
    .translate((0, 0, -clevis_thickness / 2.0))
)

# Cut the slot to form the fork/clevis shape
# The slot opens towards -X (left), leaving solid material on the +X side for the shaft
slot_cut_length = clevis_diameter
slot_cut_x_pos = -clevis_diameter / 2.0 + (clevis_diameter / 2.0 - wall_thickness) / 2.0 - clevis_diameter/2.0 # Positioning logic
# Simplified: Box centered at a calculated point to leave 'wall_thickness' on the right
slot_box = (
    cq.Workplane("XY")
    .box(clevis_diameter * 1.5, clevis_diameter * 1.5, slot_gap)
    .translate((-clevis_diameter * 0.75 + (clevis_diameter/2.0 - wall_thickness), 0, 0))
)
clevis = clevis.cut(slot_box)

# 2. Shaft
# Create the connecting rod along the X-axis
# Starts slightly inside the clevis wall to ensure solid union
shaft_start_x = clevis_diameter / 2.0 - wall_thickness
shaft = (
    cq.Workplane("YZ")
    .circle(shaft_diameter / 2.0)
    .extrude(length)
    .translate((shaft_start_x, 0, 0))
)

# 3. Rib / Gusset
# Create a triangular support rib at the junction of shaft and clevis
# Defined on XZ plane
p1 = (shaft_start_x, shaft_diameter / 2.0)
p2 = (shaft_start_x + rib_length, shaft_diameter / 2.0)
p3 = (shaft_start_x, shaft_diameter / 2.0 + rib_height)

rib = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3])
    .close()
    .extrude(2.0) # Rib thickness
    .translate((0, -1.0, 0)) # Center the rib on Y axis (2.0 / 2 = 1.0)
)

# 4. Ball End
# Create the spherical ball at the end of the shaft
ball_center_x = shaft_start_x + length
ball = (
    cq.Workplane("XY")
    .sphere(ball_diameter / 2.0)
    .translate((ball_center_x, 0, 0))
)

# 5. Wrench Flats
# Create cuts for wrench flats near the ball end
flat_center_x = ball_center_x - (ball_diameter / 2.0) - flat_offset
cut_z_offset = (shaft_diameter / 2.0) - flat_cut_depth

# Top flat cutter
flat_top = (
    cq.Workplane("XY")
    .box(flat_width, shaft_diameter * 2, shaft_diameter) # Oversized width/height
    .translate((flat_center_x, 0, cut_z_offset + shaft_diameter/2.0))
)
# Bottom flat cutter
flat_bottom = (
    cq.Workplane("XY")
    .box(flat_width, shaft_diameter * 2, shaft_diameter)
    .translate((flat_center_x, 0, -(cut_z_offset + shaft_diameter/2.0)))
)

# --- Assembly ---
result = clevis.union(shaft).union(ball).union(rib)
result = result.cut(flat_top).cut(flat_bottom)

# Export or display
# show_object(result)