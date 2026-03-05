import cadquery as cq
import math

# --- Parametric Dimensions ---
# Dimensions estimated based on a standard Metric Socket Head Cap Screw
head_diameter = 14.0      # Diameter of the screw head
head_height = 8.0         # Height of the screw head
shank_diameter = 8.0      # Diameter of the threaded shank area
shank_length = 16.0       # Length of the shank
hex_across_flats = 6.0    # Hex key size (distance across flats)
socket_depth = 4.5        # Depth of the hexagonal socket

# Calculate the circumscribed diameter for the hexagon geometry
# Relationship: Outer Diameter = Across Flats / cos(30 degrees)
hex_outer_diameter = hex_across_flats / (math.sqrt(3) / 2)

# --- 3D Modeling ---

result = (
    cq.Workplane("XY")
    # 1. Create the cylindrical head
    .circle(head_diameter / 2.0)
    .extrude(head_height)
    
    # 2. Create the hexagonal socket cut
    # Select the top face of the cylinder
    .faces(">Z")
    .workplane()
    # Create hexagon polygon (CadQuery uses circumscribed diameter)
    .polygon(6, hex_outer_diameter)
    # Cut blindly downwards into the head
    .cutBlind(-socket_depth)
    
    # 3. Create the shank
    # Select the bottom face of the head
    # Note: The normal of the bottom face points downwards (-Z)
    .faces("<Z")
    .workplane()
    .circle(shank_diameter / 2.0)
    # Extrude along the normal (downwards) to create the shank
    .extrude(shank_length)
)