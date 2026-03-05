import cadquery as cq

# Parametric definitions
total_length = 500.0  # Total length of the rod
rod_diameter = 6.0    # Diameter of the main rod body
end_diameter = 8.0    # Diameter of the ends (slightly larger caps/connectors)
end_length = 5.0      # Length of the cap/connector section at each end

# Create the main rod body
# We create a cylinder centered at the origin
main_rod = cq.Workplane("XY").circle(rod_diameter / 2.0).extrude(total_length)

# To create the caps/ends, we need to add material at the start and end.
# However, looking closely at the image, it looks like a single continuous rod
# with slightly thicker ends, or perhaps just a very long uniform rod with 
# features at the tips. The image is low resolution, but it appears to be a 
# simple shaft. Let's model it as a main shaft with distinct ends for better detail
# matching common mechanical components (like a linear rail or axle).

# Let's rebuild for a cleaner parametric structure:
# 1. Main central shaft
# 2. End caps/features

# Recalculating lengths for the assembly approach
shaft_length = total_length - (2 * end_length)

# Generate the geometry
# Start with one end cap
result = (
    cq.Workplane("XY")
    .circle(end_diameter / 2.0)
    .extrude(end_length)
    # Add the main thinner shaft
    .faces(">Z")
    .workplane()
    .circle(rod_diameter / 2.0)
    .extrude(shaft_length)
    # Add the other end cap
    .faces(">Z")
    .workplane()
    .circle(end_diameter / 2.0)
    .extrude(end_length)
)

# Note: If the image is interpreted as a simple uniform cylinder without stepped ends,
# the code would simply be: result = cq.Workplane("XY").circle(rod_diameter/2).extrude(total_length)
# Based on the "dumbbell" hint often seen in these generic CAD icons, the stepped version is safer.