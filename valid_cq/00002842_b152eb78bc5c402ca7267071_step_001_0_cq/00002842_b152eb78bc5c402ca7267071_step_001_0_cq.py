import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_width = 15.0
body_length = 40.0
body_height = 10.0

# Pin configuration
num_pins_long = 15
num_pins_short = 2  # It's a double row
pin_pitch = 2.54    # Standard breadboard/connector pitch
pin_diameter = 0.6
pin_length = 3.5

# Standoff/Spacer details (the small plastic feet under the body)
standoff_height = 1.0
standoff_width = 1.5
standoff_gap = 1.0 # Gap between standoff segments

# Location offsets
pin_offset_z = -pin_length
first_pin_x = -(body_length / 2) + (body_length - (num_pins_long - 1) * pin_pitch) / 2
first_pin_y = -(body_width / 2) + (body_width - (num_pins_short - 1) * pin_pitch) / 2


# --- Modeling ---

# 1. Main Body
# Create a simple box for the main housing
main_body = cq.Workplane("XY").box(body_length, body_width, body_height)

# Shift body up so the bottom face sits at Z=0 (easier to place pins)
main_body = main_body.translate((0, 0, body_height / 2))

# 2. Standoffs (The ribbed bottom structure)
# The image shows the bottom isn't flat; it has standoffs or a recessed area for pins.
# We will create two strips along the length where the pins emerge.
standoff_strip = (
    cq.Workplane("XY")
    .box(body_length, body_width - 2.0, standoff_height)
    .translate((0, 0, -standoff_height / 2))
)

# Cut transverse slots into the standoff strip to simulate the segmented look
# visible in the image between groups of pins
slot_width = 1.5
slot_positions = [-10, 0, 10] # Approximate locations for the visible gaps
for pos in slot_positions:
    slot = (
        cq.Workplane("XY")
        .box(slot_width, body_width, standoff_height * 2)
        .translate((pos, 0, -standoff_height / 2))
    )
    standoff_strip = standoff_strip.cut(slot)

# Combine body and standoffs
housing = main_body.union(standoff_strip)


# 3. Pins
# Create a single pin
pin = (
    cq.Workplane("XY")
    .circle(pin_diameter / 2)
    .extrude(pin_length)
    .translate((0, 0, -pin_length - standoff_height)) # Move down below the standoffs
)

# We need to array these pins.
# Since CadQuery's basic rectArray is grid-based, we'll define the grid parameters.
# The pins are usually centered relative to the body.

# Calculate the start point relative to the center
# X start: Leftmost pin position
x_span = (num_pins_long - 1) * pin_pitch
x_start = -x_span / 2

# Y start: Bottom-most pin position
y_span = (num_pins_short - 1) * pin_pitch
y_start = -y_span / 2

# Create a list of points for the pins
pin_locs = []
for i in range(num_pins_long):
    for j in range(num_pins_short):
        # We need to skip pins where the "slots" in the housing are, 
        # but looking at the image, the pins seem continuous, just the plastic is slotted.
        # Let's assume continuous pins.
        px = x_start + i * pin_pitch
        py = y_start + j * pin_pitch
        pin_locs.append((px, py))

# Generate all pins at once
pins = (
    cq.Workplane("XY")
    .pushPoints(pin_locs)
    .circle(pin_diameter / 2)
    .extrude(pin_length)
    .translate((0, 0, -pin_length)) 
)

# 4. Final Assembly
# Combine the housing and the pins
# (Often in MCAD you keep them separate bodies, but for a single mesh result we union them)
result = housing.union(pins)

# Optional: Add small location peg if visible (there seems to be a nub on the far left corner)
loc_peg = (
    cq.Workplane("XY")
    .circle(1.0)
    .extrude(2.0)
    .translate((-body_length/2 + 2, -body_width/2 + 2, -2.0))
)
result = result.union(loc_peg)