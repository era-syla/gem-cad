import cadquery as cq

# --- Parametric Variables ---
# Rail dimensions
rail_length = 300.0
rail_width = 10.0
rail_thickness = 5.0
hole_spacing = 20.0
hole_diameter = 3.5
num_holes = int(rail_length / hole_spacing) - 1

# Carriage/Slider dimensions
carriage_length = 40.0
carriage_width = 30.0
carriage_height = 15.0  # Overall height of the main block
wall_thickness = 3.0

# Carriage internal cutout (to fit the rail)
rail_slot_width = rail_width + 0.5  # Tolerance
rail_slot_depth = rail_thickness + 2.0

# Side mounting plate
side_plate_length = carriage_length + 10.0
side_plate_width = 5.0
side_plate_height = carriage_height + 20.0  # Extends down

# --- Geometry Construction ---

# 1. Create the Rail
# A simple rectangular bar
rail = cq.Workplane("XY").box(rail_width, rail_thickness, rail_length)

# Add holes to the rail
# We create a list of points along the Z-axis
hole_locations = [
    (0, 0, -rail_length/2 + hole_spacing * (i + 1)) 
    for i in range(num_holes)
]
rail = rail.faces(">Y").workplane().pushPoints(hole_locations).hole(hole_diameter)

# 2. Create the Carriage (Slider Block)
# We'll construct the carriage relative to the rail, positioned near the bottom
carriage_z_pos = -rail_length/2 + 30.0

# Base block for the carriage
carriage = (
    cq.Workplane("XY")
    .workplane(offset=carriage_z_pos)
    .box(carriage_width, carriage_height, carriage_length)
)

# Cut out the slot for the rail
# The slot goes through the carriage along Z
carriage = carriage.faces(">Z").workplane().rect(rail_slot_width, rail_slot_depth + 10).cutThruAll()

# Create the hollow sections in the carriage (lightweighting pockets)
# We assume two pockets on either side of the rail slot
pocket_width = (carriage_width - rail_slot_width - 3 * wall_thickness) / 2
pocket_length = carriage_length - 2 * wall_thickness

if pocket_width > 0:
    # Right pocket
    carriage = (
        carriage.faces(">Z")
        .workplane()
        .center((rail_slot_width/2 + wall_thickness + pocket_width/2), 0)
        .rect(pocket_width, carriage_height - 2*wall_thickness) # Cut into height (Y direction relative to local workplane)
        .cutBlind(-pocket_length) # Cut down into the length (Z direction)
    )
    # Left pocket
    carriage = (
        carriage.faces(">Z")
        .workplane()
        .center(-(rail_slot_width/2 + wall_thickness + pocket_width/2), 0)
        .rect(pocket_width, carriage_height - 2*wall_thickness)
        .cutBlind(-pocket_length)
    )

# 3. Side Mounting Plate/Bracket
# This looks like an 'L' bracket attached to one side of the carriage
bracket = (
    cq.Workplane("XY")
    .workplane(offset=carriage_z_pos - (side_plate_height - carriage_length)/2) # Shifted down relative to carriage center
    .center(-carriage_width/2 - side_plate_width/2, 0)
    .box(side_plate_width, 25.0, side_plate_height) # Height is Z, Width is X, Depth is Y
)

# Add mounting holes to the side bracket
bracket = (
    bracket.faces("<X")
    .workplane()
    .pushPoints([(0, -side_plate_height/2 + 5), (0, side_plate_height/2 - 10)])
    .hole(3.0)
)

# Small connection features or "latch" mechanism details seen in image
# Adding a small block on the other side to simulate the clamp/latch
latch = (
    cq.Workplane("XY")
    .workplane(offset=carriage_z_pos)
    .center(carriage_width/2 + 2, -5)
    .box(4, 10, 20)
)

# 4. Assemble the final result
# Union the carriage parts
carriage_assembly = carriage.union(bracket).union(latch)

# Combine rail and carriage
# The carriage is already positioned, but let's ensure they are separate bodies in a real assembly or unioned if desired as a single solid model.
# The prompt asks for a variable 'result' containing the final geometry. Usually, a single object or a compound.
result = rail.union(carriage_assembly)

# Optional: Fillets to make it look realistic
# result = result.edges("|Z").fillet(0.5)

# Ensure the result is exported/visible
if "show_object" in locals():
    show_object(result)