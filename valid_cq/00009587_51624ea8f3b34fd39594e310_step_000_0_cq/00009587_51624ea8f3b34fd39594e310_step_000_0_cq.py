import cadquery as cq

# Parametric dimensions for the lens shape
lens_width = 50.0   # Total width of one lens
lens_height = 40.0  # Total height of one lens
thickness = 2.0     # Thickness of the lens
corner_radius = 15.0 # Radius for the rounded corners (approximate)
bridge_gap = 20.0   # Distance between the two lenses

# Create a single lens profile
# We use a rectangle with rounded corners to approximate the "squircle" shape of a lens
# Alternatively, we could use splines, but a rounded rectangle is a robust parametric approximation
# for this specific geometry style.
def create_lens(x_offset):
    lens = (
        cq.Workplane("XY")
        .rect(lens_width, lens_height)
        .extrude(thickness)
        .edges("|Z") # Select vertical edges
        .fillet(corner_radius) # Round off the corners to get the organic shape
        .translate((x_offset, 0, 0)) # Position the lens
    )
    return lens

# Create the left lens
left_lens = create_lens(-lens_width/2 - bridge_gap/2)

# Create the right lens
right_lens = create_lens(lens_width/2 + bridge_gap/2)

# Combine them into the final result
result = left_lens.union(right_lens)

# Export the result (optional, but good practice for visualization)
# cq.exporters.export(result, "lenses.stl")