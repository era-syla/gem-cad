import cadquery as cq

# Parametric Dimensions
length = 100.0        # Total length of the part
width = 20.0          # Width of the part (diameter of the ends)
thickness = 5.0       # Thickness of the part
hole_diameter = 8.0   # Diameter of the holes at each end
center_dist = length - width # Distance between the centers of the circular ends

# Create the part
# We start by drawing the basic profile on the XY plane.
# A "slot" shape is the most efficient way to define this geometry in CadQuery.
# Alternatively, we could hull two circles, but let's build it step-by-step for clarity.

result = (
    cq.Workplane("XY")
    .slot2D(length, width) # Creates the racetrack shape (slot) with overall length and width
    .extrude(thickness)    # Extrude to create the solid body
    .faces(">Z")           # Select the top face
    .workplane()           # Create a new workplane on the top face
    .pushPoints([(-center_dist / 2, 0), (center_dist / 2, 0)]) # Position points for the holes
    .hole(hole_diameter)   # Cut the holes through the part
)