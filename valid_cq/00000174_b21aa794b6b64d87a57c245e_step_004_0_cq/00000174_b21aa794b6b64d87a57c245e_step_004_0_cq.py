import cadquery as cq

# Parametric definitions
nut_height = 8.0          # Total height of the nut
hex_flat_to_flat = 16.0   # Distance across flats (determines the size of the hex)
hole_diameter = 8.0       # Inner hole diameter (e.g., M8)
chamfer_angle = 30.0      # Standard chamfer angle for nuts is usually 30 degrees

# Derived dimensions
# Calculate the radius of the circle inscribing the hexagon
hex_radius = hex_flat_to_flat / (2 * 0.866025) # 0.866025 is cos(30)
# Create a slightly larger cylinder to use for the chamfer cut operation
cut_radius = hex_radius * 1.1

# 1. Create the base Hexagonal Prism
nut_body = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_radius * 2)
    .extrude(nut_height)
)

# 2. Create the Central Hole
nut_with_hole = (
    nut_body.faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# 3. Create the Chamfer Cut
# The classic "nut chamfer" is created by revolving a triangle profile 
# around the Z-axis to shave off the sharp corners of the hexagon.
# We create a profile that cuts the top corners.

# Calculate the chamfer cut geometry
# We need a profile that starts outside and cuts inwards at an angle
chamfer_cut_profile = (
    cq.Workplane("XZ", origin=(0, 0, 0))
    .moveTo(hex_flat_to_flat/2, nut_height) # Start at the edge of the flat on top
    .lineTo(cut_radius, nut_height)         # Go outwards
    .lineTo(cut_radius, 0)                  # Go down (make sure it clears the bottom if double chamfer, or just deep enough)
    .lineTo(hex_flat_to_flat/2, 0)          # Not strictly necessary to go all the way down for top chamfer only, but good practice
    .close()
)

# However, the standard conical chamfer on a nut is usually done by intersecting 
# a cone with the hex, or cutting the corners with a revolution.
# Let's create a cone shape to subtract from the top corners to get that specific arc look on the faces.

# A more robust way to get the exact "nut" look is to revolve a cutting tool.
# We want to remove material that is OUTSIDE a 30-degree cone starting from the top flat face.

# Define a cutting tool profile for the top chamfer
chamfer_size = (hex_radius - (hex_flat_to_flat/2)) * 2 # Heuristic for a nice look
chamfer_height = (hex_radius - hex_flat_to_flat/2) * 1.5 # Ensure we cut deep enough

# Create a construction plane on XZ to draw the cutting profile
# We are drawing a triangle that represents the "air" we want to keep, or the "solid" we want to remove.
# Let's subtract a shape. The shape to subtract is a ring with an angled bottom.

# Alternative approach: Revolve a cutter.
# The cutter starts at the top edge of the inscribed circle (flat-to-flat/2)
# and angles downwards and outwards.
cutter = (
    cq.Workplane("XZ")
    .moveTo(hex_flat_to_flat/2, nut_height) # Start at the top flat edge
    .lineTo(hex_radius * 1.5, nut_height)   # Go out wide
    .lineTo(hex_radius * 1.5, nut_height - chamfer_height) # Go down
    .close() # Closes back to start
    .revolve(360, (0,0,0), (0,0,1)) # Revolve around Z axis
)

# Apply the cut
result = nut_with_hole.cut(cutter)

# Optional: Usually nuts have a small internal chamfer on the thread entry as well.
# The image shows a smooth internal transition.
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(hole_diameter * 0.05)

# If the image implies a bottom chamfer (symmetric nut), we would mirror the cutter.
# The image perspective suggests a standard nut which often has chamfers on both sides, 
# but usually one side has the washer face or just identical chamfers.
# Let's apply the same logic to the bottom for a symmetrical industrial look.
cutter_bottom = (
    cq.Workplane("XZ")
    .moveTo(hex_flat_to_flat/2, 0) 
    .lineTo(hex_radius * 1.5, 0) 
    .lineTo(hex_radius * 1.5, chamfer_height) 
    .close() 
    .revolve(360, (0,0,0), (0,0,1)) 
)
result = result.cut(cutter_bottom)

# Apply filleting/chamfering to the very sharp outer hex edges if desired, 
# but standard nuts are sharp. The image shows slight softening.
# result = result.edges("|Z").fillet(0.2) 

# Export/Render
if __name__ == "__main__":
    # If running in CQ-editor, this will show the model
    try:
        show_object(result)
    except NameError:
        pass