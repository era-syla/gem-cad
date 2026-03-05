import cadquery as cq

# Define the 2D profile of the knife in the XY plane
profile_points = [
    (0, 0),       # Handle butt bottom
    (0, 15),      # Handle butt top
    (20, 15),     # Handle before first scallop
    (25, 12),     # First scallop dip
    (30, 15),     # First scallop peak
    (40, 15),     # Before second scallop
    (45, 12),     # Second scallop dip
    (50, 15),     # Second scallop peak
    (70, 15),     # End of handle
    (85, 22),     # Start of blade spine curve
    (110, 18),    # Near blade tip
    (120, 10),    # Blade tip
    (85, 0),      # Blade cutting edge back to handle bottom
    (0, 0)        # Close back at handle butt bottom
]

# Build the solid by extruding the profile
result = (
    cq.Workplane("XY")
      .polyline(profile_points)
      .close()
      .extrude(4)  # 4 mm thick blade/handle plate
)
