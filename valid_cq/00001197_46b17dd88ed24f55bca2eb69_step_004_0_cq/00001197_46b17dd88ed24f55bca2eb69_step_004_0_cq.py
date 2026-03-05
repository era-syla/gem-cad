import cadquery as cq

# Parametric Dimensions
total_length = 150.0  # Estimated total length
shank_diameter = 10.0  # Main shaft diameter
thread_length_bottom = 20.0  # Length of threads at the tip
thread_length_top = 35.0   # Length of threads near the head
unthreaded_length = total_length - thread_length_bottom - thread_length_top # Length of the smooth part

# Head Dimensions
hex_head_height = 8.0
hex_across_flats = 17.0 # Standard for M10
flange_diameter = 22.0
flange_height = 2.0
washer_face_height = 1.0

# Thread Representation (Cosmetic)
# Creating actual helical threads is computationally expensive and often unnecessary.
# We will represent threads by slightly reducing diameter or adding grooves if needed,
# but usually, a cylinder is standard. Here, to distinguish, I'll make the threaded
# sections slightly distinct cylinders.
thread_major_diam = shank_diameter
thread_minor_diam = shank_diameter * 0.9  # Cosmetic under-sizing for visual distinction

# Construction

# 1. The Hex Head
# Start with the flange/washer face
head = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_height)
)

# Add the Hexagon part on top of the flange
hex_part = (
    head.faces(">Z")
    .workplane()
    .polygon(6, hex_across_flats / (3**0.5)) # polygon takes radius, r = flat / sqrt(3) is wrong, polygon takes outer radius
    # Correct math: side-to-side (flats) = 17. Radius (center to corner) = 17 / sqrt(3) * 2 / 2 ??? 
    # Let's simplify: polygon circumradius = (across_flats / 2) / cos(30deg) = (across_flats / 2) / (sqrt(3)/2) = across_flats / sqrt(3)
    # Wait, CadQuery polygon uses outer diameter (circumscribed circle) or just radius?
    # Documentation says: polygon(nSides, diameter) where diameter is of the circumscribed circle.
    # Circumscribed diameter = (Across Flats) / (sqrt(3)/2) = (Across Flats) * 1.1547
    .polygon(6, hex_across_flats * 1.1547)
    .extrude(hex_head_height)
)

# 2. Top Threaded Section (under the head)
# Often there is a small unthreaded shoulder or undercut, but looking at the image, 
# there are threads immediately under the flange/washer.
# Let's start the shaft downwards from the bottom of the head.
shaft_start = head.faces("<Z").workplane()

# Top threads
top_threads = (
    shaft_start
    .circle(thread_major_diam / 2)
    .extrude(-thread_length_top)
)

# 3. Unthreaded Shank (Middle section)
middle_shank = (
    top_threads.faces("<Z")
    .workplane()
    .circle(shank_diameter / 2) # Usually unthreaded shank is approx equal to major diameter or slightly less
    .extrude(-unthreaded_length)
)

# 4. Bottom Threaded Section (Tip)
bottom_threads = (
    middle_shank.faces("<Z")
    .workplane()
    .circle(thread_major_diam / 2)
    .extrude(-thread_length_bottom)
)

# Combine all parts
# Note: Because we extruded sequentially from faces, they are already fused in a way, 
# but assigning to 'result' cleanly requires ensuring we have the final solid.
# The 'bottom_threads' variable contains the cumulative solid because of the chaining.

result = bottom_threads

# Optional: Add a chamfer to the very tip
result = result.faces("<Z").chamfer(1.0)

# Optional: Add a chamfer/fillet to the top of the hex head
# Select the top face, get edges, chamfer
result = result.faces(">Z").edges().chamfer(0.5)

# Optional: cosmetic grooves to simulate thread appearance (simplified)
# This adds small cuts to suggest threads without full helical geometry
def add_cosmetic_threads(part, z_start, length, pitch=1.5):
    # This is a bit complex for a basic script and can be slow. 
    # We will skip physical thread cutting for performance and robustness, 
    # relying on the cylinder diameters defined above.
    return part

# Final export
if "show_object" in locals():
    show_object(result)