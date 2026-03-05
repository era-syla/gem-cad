import cadquery as cq

# --- Parametric Dimensions ---
# Main flange plate dimensions
plate_width = 150.0   # Width of the back plate
plate_height = 200.0  # Height of the back plate
plate_thick = 5.0     # Thickness of the back plate

# Rectangular sleeve/duct dimensions
sleeve_depth = 40.0   # How far the sleeve sticks out from the plate
sleeve_wall_thick = 3.0 # Thickness of the sleeve walls
sleeve_margin = 15.0  # Margin from the plate edge to the sleeve outer edge

# Derived dimensions for the sleeve
sleeve_outer_width = plate_width - (2 * sleeve_margin)
sleeve_outer_height = plate_height - (2 * sleeve_margin)

# --- Modeling ---

# 1. Create the base plate
# We start with the full rectangular plate.
plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thick)

# 2. Create the sleeve (outer shape)
# We extrude a rectangle from the front face of the plate.
sleeve_outer = (
    cq.Workplane("XY")
    .workplane(offset=plate_thick/2) # Start from the front face of the plate
    .rect(sleeve_outer_width, sleeve_outer_height)
    .extrude(sleeve_depth)
)

# Combine the plate and the filled sleeve block
part = plate.union(sleeve_outer)

# 3. Create the through hole
# Now we cut the hole through the entire assembly to make it a frame.
# The hole size corresponds to the inner dimensions of the sleeve.
hole_width = sleeve_outer_width - (2 * sleeve_wall_thick)
hole_height = sleeve_outer_height - (2 * sleeve_wall_thick)

# We cut through everything. The cut depth needs to be sufficient.
# Total thickness = plate_thick/2 + sleeve_depth + extra for safety
cut_depth = plate_thick + sleeve_depth + 10.0

result = (
    part.faces(">Z") # Select the front face of the sleeve
    .workplane()
    .rect(hole_width, hole_height)
    .cutBlind(-cut_depth)
)

# Validating the result object
# (This is implicitly returned as 'result' for the user)