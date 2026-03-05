import cadquery as cq

# --- Parametric Dimensions ---
length = 150.0       # Total length of the part
width = 24.0         # Outer width
height = 14.0        # Height of the side flanges
thickness = 1.5      # Material thickness
bend_start = 110.0   # X-coordinate where the tail starts to angle up
tip_rise = 10.0      # Vertical rise of the tail end

# --- 1. Side Flange Construction ---

# Define the profile polygon for the side wall on the XZ plane.
# This captures the straight section and the angled tail.
pts = [
    (0, 0),
    (bend_start, 0),             # Start of upward bend (bottom)
    (length, tip_rise),          # Tip (bottom)
    (length, tip_rise + height), # Tip (top)
    (bend_start, height),        # End of upward bend (top)
    (0, height)                  # Back to start
]

# Create the base solid for the left flange
# Extruded along +Y
left_flange = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# --- 2. Adding Features (Cuts) to Side Flange ---

# Define a workplane on the side face for cutting features
# We look at the face with normal +Y
cuts_plane = left_flange.faces(">Y").workplane()

# Feature 1: Circular hole near the front
cuts_plane = (
    cuts_plane
    .moveTo(6, height / 2.0)
    .circle(1.8)
    .cutThruAll()
)

# Feature 2: Rectangular notch on the top edge (approx 1/3 length)
cuts_plane = (
    cuts_plane
    .moveTo(45, height)
    .rect(10.0, 6.0, centered=True)  # Depth approx 3mm
    .cutThruAll()
)

# Feature 3: Rectangular slot in the side wall (approx middle)
cuts_plane = (
    cuts_plane
    .moveTo(65, height / 2.0 - 1.0)
    .rect(12.0, 5.0)
    .cutThruAll()
)

# Feature 4: Small notch/tab on top edge (near slot)
cuts_plane = (
    cuts_plane
    .moveTo(85, height)
    .rect(5.0, 4.0, centered=True)
    .cutThruAll()
)

# Feature 5: Circular hole before the bend
cuts_plane = (
    cuts_plane
    .moveTo(bend_start - 10.0, height / 2.0)
    .circle(1.8)
    .cutThruAll()
)

# Feature 6: The Fork/Hook at the tip
# Modeled as a circular cutout that breaks through the top-back edge
fork_center_x = length - 2.0
fork_center_z = tip_rise + height - 3.0
fork_radius = 3.5

# Cut the circular hook shape
cuts_plane = (
    cuts_plane
    .moveTo(fork_center_x, fork_center_z)
    .circle(fork_radius)
    .cutThruAll()
)

# Clear material above the circle to form the U-shape opening
cuts_plane = (
    cuts_plane
    .moveTo(fork_center_x, fork_center_z + fork_radius)
    .rect(fork_radius * 2.5, fork_radius * 2.5)
    .cutThruAll()
)

# Update the left_flange with all cuts
left_flange = cuts_plane.val() # Get the underlying solid

# --- 3. Assembly and Mirroring ---

# Create Right Flange
# Since the part is a U-channel, the right side is a translation of the left side.
# Left flange occupies Y=[0, thickness].
# Right flange needs to occupy Y=[width-thickness, width].
right_flange = (
    cq.Workplane("XY") # Dummy plane to start new chain
    .add(left_flange)
    .translate((0, width - thickness, 0))
)

# Create Bottom Web
# The bottom plate connects the two flanges.
# It typically stops where the flanges bend upwards (based on the image).
# Fits strictly between the flanges to simulate sheet metal bending.
bottom_web = (
    cq.Workplane("XY")
    .moveTo(bend_start / 2.0, width / 2.0)
    .rect(bend_start, width - 2 * thickness)
    .extrude(thickness)
)

# Union the parts
# left_flange (Solid), right_flange (Workplane object), bottom_web (Workplane object)
# Convert all to solids for union
result = (
    cq.Workplane("XY")
    .add(left_flange)
    .union(right_flange)
    .union(bottom_web)
)