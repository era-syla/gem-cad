import cadquery as cq

# --- Parameters ---
# Dimensions for the overall plate
plate_width = 100.0   # Total width of the square plate
plate_height = 100.0  # Total height of the square plate
base_thickness = 2.0  # Thickness of the solid base underneath the pyramids

# Grid parameters
num_x = 10  # Number of pyramids along the X axis
num_y = 10  # Number of pyramids along the Y axis

# Derived parameters
cell_width = plate_width / num_x
cell_height = plate_height / num_y
pyramid_height = cell_width * 0.4  # Height of each pyramid, proportional to its base

# --- Modeling ---

# 1. Create the base plate
# We start with a simple box that serves as the substrate.
base = cq.Workplane("XY").box(plate_width, plate_height, base_thickness)

# 2. Create a single pyramid unit
# We'll create a pyramid by lofting from a square base to a point (or very small square)
# or by creating a solid wedge. A loft is a robust way to do this.
# The pyramid sits on top of the base, so we start its construction plane on top of the base.

# Define the base rectangle of the pyramid
pyramid_unit = (
    cq.Workplane("XY")
    .rect(cell_width, cell_height)
    .workplane(offset=pyramid_height)
    .rect(0.001, 0.001) # Effectively a point top
    .loft(combine=True)
)

# 3. Create the grid of pyramids
# We will create points for the grid locations.
# The center of the plate is (0,0).
# We need to calculate the step size and start positions.
# CadQuery's rarray (rectangular array) is perfect for this.

# Generate the grid of pyramids
pyramids = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=cell_width, 
        ySpacing=cell_height, 
        xCount=num_x, 
        yCount=num_y, 
        center=True
    )
    .eachpoint(lambda loc: pyramid_unit.val().moved(loc))
)

# 4. Combine everything
# The base is centered at Z=0 (spanning -thickness/2 to +thickness/2).
# We need to move the pyramids so their base sits exactly on the top face of the base plate.
# The top of the base plate is at Z = base_thickness / 2.
# The pyramids were created on the XY plane (Z=0).
# So we need to translate the pyramids up by base_thickness / 2.

# Convert the list of pyramid solids into a Compound
pyramid_compound = cq.Compound.makeCompound(pyramids)

# Translate the compound to sit on top of the base
pyramid_compound = pyramid_compound.translate((0, 0, base_thickness / 2))

# Union the base and the pyramids
result = base.union(pyramid_compound)

# If running in an environment that supports show_object (like CQ-Editor), this line helps visualize
# show_object(result) 