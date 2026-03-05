import cadquery as cq

# Parameters
outer_diameter = 50.0   # Overall diameter of the cap
height = 15.0           # Overall height of the cap
wall_thickness = 1.5    # Thickness of the material
hole_diameter = 4.0     # Diameter of the 4 holes on top
hole_spacing = 25.0     # Distance between hole centers (square pattern size)

# Slot parameters
slot_width = 8.0        # Width of the rectangular cutouts on the skirt
slot_height = 10.0      # Height of the cutout from the bottom edge
slot_count = 4          # Number of slots around the perimeter

# Create the base cylindrical shell
# 1. Create a solid cylinder
# 2. Hollow it out to create the "cap" shape
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .faces(">Z")
    .shell(-wall_thickness)
)

# Create the 4 holes on the top face
# We select the top face, work on it, push points in a square pattern, and cut holes
result = (
    base
    .faces(">Z")
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# Create the slots on the side skirt
# We need to cut rectangular slots starting from the bottom edge
# A polar array approach works best for radial symmetry
for i in range(slot_count):
    # Calculate rotation angle for each slot
    angle = i * (360.0 / slot_count)
    
    # Create a cutting tool for the slot
    # Position a rectangle on a plane tangent to the side or simply cut through from the side
    # Here we define a profile on the XZ plane, move it out to the radius, rotate it, and cut
    
    # Alternative strategy: Select the bottom face, create a workplane, 
    # transform to the side, and cut.
    
    # Simple robust strategy: Create a box shape and cut it away from the main body
    cutter = (
        cq.Workplane("XY")
        .box(outer_diameter + 10, slot_width, slot_height) # Make box wider than diameter
        .translate((0, 0, slot_height / 2.0)) # Align bottom of box with Z=0
        .rotate((0,0,1), (0,0,0), angle) # Rotate around Z axis
    )
    
    result = result.cut(cutter)

# Final result is stored in the variable 'result' as requested