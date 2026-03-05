import cadquery as cq

# Parameters defining the dimensions of the part
length = 300.0        # Total length of the bar (X direction)
height = 40.0         # Height of the strip (Extrusion length in Z direction)
thickness = 3.0       # Thickness of the material
offset_depth = 15.0   # Depth of the offset step (Y direction)
flange_length = 15.0  # Length of the tabs at both ends

# Half-length for coordinate calculations
x_half = length / 2.0

# Define vertices for the cross-section profile in the XY plane
# The profile traces the "Hat" shape
# Logic assumes the vertical legs consume space from the flange length (eating into the flange)

# Points for the profile (Counter-Clockwise direction)
points = [
    # Inner/Bottom surface path
    (-x_half, 0),                                      # Start at bottom-left corner
    (-x_half + flange_length, 0),                      # End of left inner flange
    (-x_half + flange_length, offset_depth - thickness), # Bottom of left step (vertical up)
    (x_half - flange_length, offset_depth - thickness),  # Start of right step (horizontal web)
    (x_half - flange_length, 0),                       # Bottom of right step (vertical down)
    (x_half, 0),                                       # End of right inner flange
    
    # Outer/Top surface path (Thickness added)
    (x_half, thickness),                               # Thickness at right end
    (x_half - flange_length + thickness, thickness),   # Corner of right leg/flange
    (x_half - flange_length + thickness, offset_depth),# Corner of right leg/web
    (-x_half + flange_length - thickness, offset_depth),# Corner of left leg/web
    (-x_half + flange_length - thickness, thickness),  # Corner of left leg/flange
    (-x_half, thickness)                               # Thickness at left end
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(height)
)