import cadquery as cq

# --- Parametric Dimensions ---
height_total = 32.0
head_diam = 13.0
head_height = 4.0
shaft_diam = 6.0
shaft_height = 12.0
base_diam = 11.0
base_widest_h = 4.5
neck_h = 13.0  # Height where the neck curve meets the straight shaft

# Derived parameters
r_head = head_diam / 2.0
r_shaft = shaft_diam / 2.0
r_base = base_diam / 2.0
r_base_flat = 3.5  # Radius of the flat spot at the very bottom

# --- Create Main Body (Revolution) ---
# We define the profile on the XZ plane (right side) and revolve it.
# The profile includes the flat bottom, the bulbous base, the neck transition,
# the straight shaft, and the countersunk head.

# Define critical points
p0 = (0, 0)                         # Center bottom
p1 = (r_base_flat, 0)               # Edge of flat bottom
p2 = (r_base, base_widest_h)        # Widest point of the base bulb
p3 = (r_shaft, neck_h)              # Start of straight shaft (top of neck)
p4 = (r_shaft, height_total - head_height) # Top of shaft / bottom of head
p5 = (r_head, height_total)         # Top outer rim of head
p6 = (0, height_total)              # Top center

# Construct the wire profile
# We use a spline to create the organic smooth transition from the base to the shaft (the neck)
profile = (
    cq.Workplane("XZ")
    .moveTo(*p0)
    .lineTo(*p1)
    .spline(
        [p2, p3], 
        tangents=[(1, 0.3), (0, 1)], # Tangent out flat-ish, tangent in vertical
        includeCurrent=True
    )
    .lineTo(*p4)
    .lineTo(*p5)
    .lineTo(*p6)
    .close()
)

# Revolve to create the solid
main_body = profile.revolve()

# --- Create Phillips Driver Recess ---
# We create a cross shape on the top face and cut it into the body.
drive_span = 6.5
drive_width = 1.4
drive_depth = 2.5

# Create the cutting tool shape (Cross)
# We extrude with a taper to simulate a realistic driver impression
driver_tool = (
    cq.Workplane("XY")
    .workplane(offset=height_total)
    .rect(drive_span, drive_width)
    .rect(drive_width, drive_span)
    .clean() # Merge the two rectangles into a single cross wire
    .extrude(-drive_depth, taper=20) # Extrude down with draft angle
)

# --- Final Boolean Operation ---
result = main_body.cut(driver_tool)