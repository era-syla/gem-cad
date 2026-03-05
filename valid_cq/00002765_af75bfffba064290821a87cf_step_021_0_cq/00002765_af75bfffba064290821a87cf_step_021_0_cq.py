import cadquery as cq

# Parametric dimensions for a standard Socket Head Cap Screw (e.g., M5 x 50)
thread_diameter = 5.0  # Diameter of the threaded part
total_length = 50.0  # Length from under the head to the end
thread_length = 20.0  # Length of the threaded section
head_diameter = 8.5  # Diameter of the cylindrical head
head_height = 5.0    # Height of the head
hex_socket_size = 4.0 # Size of the hexagonal socket (across flats)
socket_depth = 3.0   # Depth of the hexagonal socket
chamfer_size = 0.5   # Chamfer at the tip of the screw
fillet_radius = 0.2  # Small fillet under the head for stress relief

# Create the Screw Shaft
# We start with the unthreaded shank portion
shank_length = total_length - thread_length
shank = cq.Workplane("XY").circle(thread_diameter / 2).extrude(shank_length)

# Create the Threaded Section (represented as a cylinder for simplicity in standard CAD,
# but we will add a visual representation of threads or just the cylinder)
# Since specific thread modeling can be computationally heavy, we will model the 
# threaded part as a cylinder with a slightly smaller diameter to represent the minor diameter,
# or keep it nominal. Let's keep it nominal but potentially add a cosmetic texture feature if needed.
# For a robust CAD model, a cylinder is standard.
threaded_part = (
    cq.Workplane("XY")
    .workplane(offset=shank_length)
    .circle(thread_diameter / 2)
    .extrude(thread_length)
)

# Combine Shank and Threaded Part
bolt_body = shank.union(threaded_part)

# Add chamfer to the tip
bolt_body = bolt_body.faces(">Z").chamfer(chamfer_size)

# Create the Head
head = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at the bottom of the shank (Z=0)
    .circle(head_diameter / 2)
    .extrude(-head_height) # Extrude downwards
)

# Combine Body and Head
bolt = bolt_body.union(head)

# Create the Hex Socket
# We need to cut a hexagon into the top face of the head (which is at Z = -head_height relative to shank start,
# but let's re-orient for clarity. The head is currently at the bottom in Z-negative).
# The head's "top" face (where the tool goes) is at Z = -head_height.
bolt = (
    bolt.faces("<Z") # Select the bottom-most face (which is the top of the head in this orientation)
    .workplane()
    .polygon(6, hex_socket_size / 0.866025, circumscribed=True) # 0.866 is cos(30), converting flat-to-flat to diameter
    .cutBlind(socket_depth)
)

# Add fillet under the head (where head meets shank)
# We need to select the edge at the intersection of the head face and the shank cylinder.
# The shank starts at Z=0. The head ends at Z=0.
bolt = bolt.edges(cq.selectors.RadiusNthSelector(1)).fillet(fillet_radius)

# Optional: Add simplified thread representation (Helical cut) 
# Note: Real threads are expensive. This adds a simple visual spiral cut.
# To make it robust and run fast, we often skip this, but the prompt implies visual similarity.
# Let's create a visual approximation using a spiral cut on the threaded section.
path = cq.Workplane("XY").workplane(offset=shank_length).parametricCurve(
    lambda t: (
        (thread_diameter/2) * 1.0, 
        (thread_length * t) * 0, # Placeholder for proper helix generation if needed, simpler to skip for stability
        (thread_length * t)
    )
)

# Given the complexity of helical sweeps in pure code without external libraries, 
# a common convention is to just return the solid geometry.
# However, to match the image which shows texture, let's add a series of small circular grooves 
# to simulate threads visually without the overhead of a helix.

pitch = 0.8
groove_depth = 0.15
num_turns = int(thread_length / pitch)

for i in range(num_turns):
    z_pos = shank_length + (i * pitch) + (pitch/2)
    # Don't cut too close to the chamfered tip
    if z_pos < (total_length - chamfer_size):
        # Create a cutting tool for a single groove
        groove = (
            cq.Workplane("XZ")
            .workplane(offset=z_pos)
            .moveTo(thread_diameter / 2, 0)
            .lineTo(thread_diameter / 2 - groove_depth, 0)
            .lineTo(thread_diameter / 2, pitch/2)
            .close()
            .revolve(360, (0,0,0), (0,0,1))
        )
        bolt = bolt.cut(groove)

# Re-orient the bolt so it stands up like the image (Head at bottom, threads up)
# Currently: Head is Z-negative, Tip is Z-positive.
# We want Head at Z=0, Tip at Z-positive.
result = bolt.translate((0, 0, head_height))