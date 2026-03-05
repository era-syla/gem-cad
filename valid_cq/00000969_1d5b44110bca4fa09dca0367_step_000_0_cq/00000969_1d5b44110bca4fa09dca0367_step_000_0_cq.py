import cadquery as cq

# --- Parameter Definitions ---
height = 100.0   # Height of the plates
width = 100.0    # Width (length) of the plates
thickness = 5.0  # Thickness of each plate
gap = 40.0       # Distance between the two plates

# --- Modeling ---

# Create the first plate
# We start by sketching on the XY plane, creating a rectangle centered on X and Y
plate1 = (
    cq.Workplane("XY")
    .box(width, thickness, height)
    .translate((0, -gap / 2 - thickness / 2, 0))
)

# Create the second plate
# Similar to the first, but offset in the positive Y direction
plate2 = (
    cq.Workplane("XY")
    .box(width, thickness, height)
    .translate((0, gap / 2 + thickness / 2, 0))
)

# Combine the two separate solids into a single compound object
result = plate1.union(plate2)

# If running in an environment that supports show_object (like CQ-editor), this helps visualize
# show_object(result)