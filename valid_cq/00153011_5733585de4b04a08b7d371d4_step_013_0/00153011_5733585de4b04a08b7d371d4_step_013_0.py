import cadquery as cq

# --- Parametric Dimensions ---
# Radii
r_inner = 35.0
r_step = 45.0          # Radius where the thickness changes
r_outer_flat = 50.0    # Radius where the outer curve starts
r_outer_max = 55.0     # Maximum outer radius (apex of curve)

# Heights (Z coordinates relative to bottom of inner shelf)
h_shelf_base = 0.0
h_shelf_top = 4.0
h_rim_bottom = -2.5    # Outer rim extends downwards
h_rim_top = 7.0        # Outer rim extends upwards

# Angular extent of the segment
angle_total = 115.0

# Pin parameters
pin_dia_base = 3.5
pin_dia_top = 2.5
pin_height = 5.0
pin_angle_from_end = 20.0  # Position relative to the end of the arc

# Notch parameters (right end cut)
notch_size = 3.5

# --- 1. Create Cross-Section Profile ---
# Define points for the profile in XZ plane (Clockwise)
p_inner_bot = (r_inner, h_shelf_base)
p_inner_top = (r_inner, h_shelf_top)
p_step_top_inner = (r_step, h_shelf_top)
p_step_top_outer = (r_step, h_rim_top)
p_rim_top_edge = (r_outer_flat, h_rim_top)
p_rim_mid_apex = (r_outer_max, (h_rim_top + h_rim_bottom) / 2.0)
p_rim_bot_edge = (r_outer_flat, h_rim_bottom)
p_step_bot_outer = (r_step, h_rim_bottom)
p_step_bot_inner = (r_step, h_shelf_base)

# Build the sketch
sketch = (
    cq.Sketch()
    .segment(p_inner_bot, p_inner_top)
    .segment(p_step_top_inner)
    .segment(p_step_top_outer)
    .segment(p_rim_top_edge)
    .arc(p_rim_mid_apex, p_rim_bot_edge)  # Bulbous outer profile
    .segment(p_step_bot_outer)
    .segment(p_step_bot_inner)
    .close()
    .assemble()
    .vertices(cq.NearestToPointSelector(p_inner_top)).fillet(0.5)
    .vertices(cq.NearestToPointSelector(p_step_top_inner)).fillet(1.0)
    .vertices(cq.NearestToPointSelector(p_step_top_outer)).fillet(1.5)
    .vertices(cq.NearestToPointSelector(p_rim_top_edge)).fillet(3.0)
    .vertices(cq.NearestToPointSelector(p_rim_bot_edge)).fillet(3.0)
    .vertices(cq.NearestToPointSelector(p_step_bot_outer)).fillet(1.0)
    .vertices(cq.NearestToPointSelector(p_step_bot_inner)).fillet(1.0)
)

# --- 2. Revolve Main Body ---
main_body = cq.Workplane("XZ").placeSketch(sketch).revolve(angle_total)

# --- 3. Create and Place the Pin ---
# Create cone along Z axis
pin_solid = cq.Solid.makeCone(pin_dia_base / 2.0, pin_dia_top / 2.0, pin_height)

# Add fillet to the top of the pin
pin_wp = cq.Workplane(obj=pin_solid).edges(cq.NearestToPointSelector((0, 0, pin_height))).fillet(0.5)
pin_solid = pin_wp.val()

# Orient pin to point along X axis
pin_solid = pin_solid.rotate((0, 0, 0), (0, 1, 0), 90)

# Translate to correct radial and vertical position
pin_z_center = (h_rim_top + h_rim_bottom) / 2.0
pin_solid = pin_solid.translate((r_outer_max - 0.5, 0, pin_z_center))

# Rotate to final angular position around Z axis
pin_angle = angle_total - pin_angle_from_end
pin_solid = pin_solid.rotate((0, 0, 0), (0, 0, 1), pin_angle)

# --- 4. Create End Cutout (Notch) ---
# Create a box to cut the bottom-outer corner of the end face
# Box dimensions should be large enough to clear the corner
cut_tool = cq.Solid.makeBox(10, 10, 10)

# Position the box to cut a rebate of 'notch_size' from the corner
# Translate X to start at (Radius - notch_size)
# Translate Z to start at (Height_bottom)
cut_tool = cut_tool.translate((r_outer_max - notch_size, -5, h_rim_bottom))

# Rotate tool to align with the end face plane
cut_tool = cut_tool.rotate((0, 0, 0), (0, 0, 1), angle_total)

# --- 5. Combine Operations ---
result = (
    main_body
    .union(cq.Workplane(obj=pin_solid))
    .cut(cq.Workplane(obj=cut_tool))
)