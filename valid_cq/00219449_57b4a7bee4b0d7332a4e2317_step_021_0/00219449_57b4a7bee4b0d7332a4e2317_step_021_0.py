import cadquery as cq

# --- Parameters ---
# Dimensions based on EIA-310 standard for server rack rails
num_units = 42              # Number of Rack Units (U) - 42U is a standard full-height rack
u_height = 44.45            # Height of one rack unit (1.75 inches) in mm
rail_width = 19.05          # Width of the rail strip (0.75 inches)
rail_thickness = 2.0        # Thickness of the material
hole_size = 9.525           # Square hole size for cage nuts (0.375 inches)
rail_separation = 465.1     # Center-to-center distance between rails (approx 18.31 inches)

# Calculated total height
total_height = num_units * u_height

# --- Geometry Generation ---

# Generate the list of hole center points
# The pattern within one 1U (44.45mm) height repeats:
# Hole 1: 0.25" (6.35mm) from bottom
# Hole 2: 0.875" (22.225mm) from bottom (spacing 0.625")
# Hole 3: 1.500" (38.1mm) from bottom (spacing 0.625")
# Gap to next unit: 0.500" (12.7mm)

hole_points = []
start_z = -total_height / 2  # Start from the bottom of the geometry

for i in range(num_units):
    unit_base_z = start_z + (i * u_height)
    
    # Offsets defined by standard
    offsets = [6.35, 22.225, 38.1]
    
    for offset in offsets:
        # Points are (x, y) on the 2D workplane. 
        # Since we will sketch on the front face, y on sketch maps to z in global.
        hole_points.append((0, unit_base_z + offset))

# Create the base rail geometry
# We create a box centered on the origin, then select the front face to cut holes
rail = (
    cq.Workplane("XY")
    .box(rail_width, rail_thickness, total_height)
    .faces(">Y")              # Select the front face (positive Y)
    .workplane()              # Create a 2D workplane on this face
    .pushPoints(hole_points)  # Place points for all holes
    .rect(hole_size, hole_size) # Sketch square holes
    .cutThruAll()             # Cut them through the rail
)

# Create the pair of rails by positioning the single rail
left_rail = rail.translate((-rail_separation / 2, 0, 0))
right_rail = rail.translate((rail_separation / 2, 0, 0))

# Combine into the final result
result = left_rail.union(right_rail)