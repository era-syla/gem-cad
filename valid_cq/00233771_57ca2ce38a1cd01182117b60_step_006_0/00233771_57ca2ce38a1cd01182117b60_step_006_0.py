import cadquery as cq

# --- Geometric Parameters ---
# Pin dimensions (Unit: mm)
pin_diameter = 5.0
pin_radius = pin_diameter / 2.0
pin_len_long = 70.0
pin_len_short = 45.0

# Groove parameters for the pins
groove_width = 1.0
groove_depth = 0.4
groove_offset_from_end = 2.5

# Bushing dimensions
bush_od = 12.0
bush_id = 8.0
bush_length = 20.0

# Layout spacing parameters
vertical_spacing = 25.0
horizontal_shift = 20.0

# --- Helper Functions ---

def create_grooved_pin(length, radius, g_width, g_depth, g_offset):
    """
    Creates a cylindrical pin with retaining ring grooves at both ends.
    Aligned along the X-axis, centered at the origin.
    """
    # Create main shaft
    # Using YZ plane allows extrusion along the X-axis
    pin = cq.Workplane("YZ").circle(radius).extrude(length / 2.0, both=True)
    
    # Create the cutting tool for the groove (a ring shape)
    # We define a tube that intersects the pin surface
    cutter_r_inner = radius - g_depth
    cutter_r_outer = radius + 1.0  # Clearance
    
    cutter = (cq.Workplane("YZ")
              .circle(cutter_r_outer)
              .circle(cutter_r_inner)
              .extrude(g_width / 2.0, both=True))
    
    # Calculate position X coordinate for the grooves
    # Pin is centered at 0, so ends are at +/- length/2
    gx = (length / 2.0) - g_offset - (g_width / 2.0)
    
    # Cut grooves at both ends
    pin = pin.cut(cutter.translate((gx, 0, 0)))
    pin = pin.cut(cutter.translate((-gx, 0, 0)))
    
    # Chamfer the ends of the pin
    pin = pin.faces("<X or >X").chamfer(0.3)
    
    return pin

def create_bushing(od, id, length):
    """
    Creates a hollow bushing.
    Aligned along the X-axis, centered at the origin.
    """
    bush = (cq.Workplane("YZ")
            .circle(od / 2.0)
            .circle(id / 2.0)
            .extrude(length / 2.0, both=True))
    
    # Chamfer the outer edges
    bush = bush.faces("<X or >X").chamfer(0.5)
    return bush

# --- Model Generation & Assembly ---

# 1. Top Long Pin
pin_top = create_grooved_pin(
    pin_len_long, pin_radius, groove_width, groove_depth, groove_offset_from_end
).translate((0, vertical_spacing, 0))

# 2. Middle Long Pin
pin_mid = create_grooved_pin(
    pin_len_long, pin_radius, groove_width, groove_depth, groove_offset_from_end
).translate((0, 0, 0))

# 3. Bottom Right Short Pin
pin_short = create_grooved_pin(
    pin_len_short, pin_radius, groove_width, groove_depth, groove_offset_from_end
).translate((horizontal_shift, -vertical_spacing, 0))

# 4. Bottom Left Bushing
bushing = create_bushing(
    bush_od, bush_id, bush_length
).translate((-horizontal_shift * 1.5, -vertical_spacing, 0))

# Combine all parts into a single result object
result = pin_top.union(pin_mid).union(pin_short).union(bushing)

# For visualization in CQ-editor or similar environments
if 'show_object' in globals():
    show_object(result)