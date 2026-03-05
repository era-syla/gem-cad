import cadquery as cq
import math

# --- Parameters ---
outer_radius = 20.0       # Radius of the main cylinder
inner_radius = 15.0       # Radius of the main central hole
total_height = 35.0       # Total height of the part
wall_thickness = 4.0      # Thickness of the bottom wall (or flange lip depth)
hole_radius = 10.0        # Radius of the smaller hole at the bottom

# Castellation parameters (the notches on the top)
num_notches = 4           # Number of notches (looks like 4 based on symmetry)
notch_width = 8.0         # Width of the rectangular cutout
notch_depth = 8.0         # Depth of the cutout from the top edge

# --- Modeling ---

# 1. Create the main cylindrical body
# We start with a solid cylinder
body = cq.Workplane("XY").circle(outer_radius).extrude(total_height)

# 2. Create the main internal bore (blind hole or through hole depending on interpretation)
# Looking at the image, it seems to have a stepped hole. A larger diameter at the top,
# stepping down to a smaller diameter at the bottom.
# Let's cut the large bore first from the top face down.
large_bore_depth = total_height - wall_thickness
body = body.faces(">Z").workplane().hole(inner_radius * 2, large_bore_depth)

# 3. Create the smaller through-hole at the bottom
body = body.faces("<Z").workplane().hole(hole_radius * 2)

# 4. Create the Castellations (Notches)
# We need to cut rectangular notches from the top rim.
# We will create one notch profile and polar array it.

# Create a cutter for the notches
# We place a rectangle on the top face, offset from center so it cuts the rim
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height) # Move to top
    .transformed(rotate=(0, 0, 45)) # Rotate so notches aren't aligned with X/Y axes initially if desired, or just to match visual
    .rect(notch_width, outer_radius * 3) # Make rectangle long enough to cut through the wall
    .extrude(-notch_depth) # Cut downwards
)

# Apply the cut in a polar pattern
# Since CadQuery's cut operation doesn't support direct polar array of the tool easily in one line without
# constructing the tool first, let's use the 'cut' method with a rotated shape or use a sketch approach.
# A robust way is to sketch on the top face.

def notch_sketch(loc):
    return cq.Sketch().rect(notch_width, outer_radius * 3)

body = (
    body.faces(">Z")
    .workplane()
    .polarArray(outer_radius, 0, 360, num_notches)
    .rect(notch_width, outer_radius * 3) # Draw rectangles
    .cutBlind(-notch_depth) # Cut them down
)

# 5. Optional: Fillets or Chamfers
# The image shows a very slight chamfer or deburring on the top edge, 
# and potentially a fillet inside. Let's add a small chamfer to the outer top edge 
# and the inner top edge for realism.

# Select the top outer edge
body = body.edges(">Z and %circle").chamfer(0.5)

# 6. Final Result
result = body