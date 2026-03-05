import cadquery as cq

# -- Parametric Dimensions --
total_height = 100.0      # Total vertical height of the part
width_top = 20.0          # Width at the widest point (start of the top arc)
width_bottom = 10.0       # Width at the bottom base
thickness = 5.0           # Constant thickness of the material
hole_width = 6.0          # Width of the rectangular slot
hole_height = 4.0         # Height of the rectangular slot
hole_top_offset = 10.0    # Distance from the very top tip to the center of the hole

# -- Derived Geometry Calculations --
# The top is a semi-circle, so its radius is half the top width
radius = width_top / 2.0
# Calculate the height where the straight tapered section ends
h_straight = total_height - radius
# Calculate the Z coordinate for the center of the hole
hole_z = total_height - hole_top_offset

# -- Model Construction --
# Create the base shape on the XZ plane so "Height" corresponds to the Z-axis
result = (
    cq.Workplane("XZ")
    # Define the profile path
    .moveTo(-width_bottom / 2.0, 0)
    .lineTo(width_bottom / 2.0, 0)                  # Bottom edge
    .lineTo(width_top / 2.0, h_straight)            # Right tapered edge
    # Create the top semi-circle using a 3-point arc:
    # 1. Current point (start) is implicitly (width_top/2, h_straight)
    # 2. Pass through the peak at (0, total_height)
    # 3. End at (-width_top/2, h_straight)
    .threePointArc((0, total_height), (-width_top / 2.0, h_straight))
    .lineTo(-width_bottom / 2.0, 0)                 # Left tapered edge
    .close()
    # Extrude symmetrically to create the thickness
    .extrude(thickness / 2.0, both=True)
)

# Create the rectangular hole
result = (
    result
    .faces(">Y")                                    # Select the front face
    .workplane(centerOption="ProjectedOrigin")      # Use global origin projected onto face
    .moveTo(0, hole_z)                              # Move to hole center
    .rect(hole_width, hole_height)                  # Sketch the rectangle
    .cutThruAll()                                   # Cut through the entire part
)