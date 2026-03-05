import cadquery as cq

# --- Parameter Definitions ---
height = 100.0       # Total height of the tube
outer_diameter = 30.0 # Outer diameter of the main tube
wall_thickness = 1.0  # Thickness of the tube wall
hole_diameter = 10.0  # Diameter of the side hole
hole_height_ratio = 0.7 # Approximate vertical position of the hole (0.0 to 1.0)

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
hole_center_z = height * hole_height_ratio

# --- Modeling ---

# 1. Create the main hollow cylinder (tube)
# We extrude a ring profile
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# 2. Cut the side hole
# We create a workplane tangent to the side or perpendicular to the Z axis at the specific height
# A simple way is to use a YZ or XZ plane, move it up, and cut through.
result = (
    result
    .faces(">Z") # Select top face to establish relative orientation if needed, though direct workplanes are safer
    .workplane(centerOption="CenterOfMass") # Reset to center
    .transformed(offset=cq.Vector(0, 0, - (height - hole_center_z))) # Move down from top (since extrude was up) OR easier: start fresh from XZ
)

# Alternative, cleaner approach for the hole:
# Select the XZ plane, move to the correct height, and cut a cylinder through the object.
hole_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=0) # Center of the object
    .center(0, hole_center_z) # Position the hole vertically
    .circle(hole_diameter / 2.0)
    .extrude(outer_diameter + 10.0, both=True) # Extrude enough to cut through everything
)

result = result.cut(hole_cutter)

# Export or visualization would happen here normally, but 'result' is the required variable.