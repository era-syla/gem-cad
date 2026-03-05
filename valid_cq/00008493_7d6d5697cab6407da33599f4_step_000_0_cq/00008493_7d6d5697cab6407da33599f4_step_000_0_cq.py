import cadquery as cq

# --- Parameters ---
# Overall dimensions
total_height = 1000.0  # Total height of the post
width = 50.0          # Width of the square profile
depth = 50.0          # Depth of the square profile
wall_thickness = 3.0  # Thickness of the tube walls

# Bottom section (black part) dimensions
base_height = 150.0   # Height of the darker base section

# --- Modeling ---

# Create the main hollow tube (the long grey part)
# We'll make it the full length first
tube = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(total_height)
    # Make it hollow
    .faces(">Z").shell(-wall_thickness)
)

# Create the base section (the black part)
# It appears to be slightly larger or a sleeve, or just a different finish.
# Assuming it's a solid block or a slightly thicker sleeve at the bottom.
# Based on the visual, it fits flush with the tube but is distinct.
# Let's model it as a solid base plug or a reinforced bottom section.
# Given it looks like a post, often the bottom is a solid anchor or a sleeve.
# Let's model it as a solid block at the bottom for structural integrity, 
# distinct from the tube, but united in the final result.

# Option A: It's just a colored section of the same tube.
# Option B: It's a separate solid base. 
# Looking closely at the junction, it's flush. Let's assume it's a solid base insert 
# or the tube is simply filled/solid at the bottom, or it's a sleeve.
# However, for a single solid geometry result in CAD, we typically union them.

# Let's refine: The image shows a hollow top. The bottom is black.
# It's safest to model the entire thing as the tube, and then create the bottom
# detail. The bottom looks like it might have a small hole or fastener detail on the side.
# Let's add a small hole near the bottom as seen in the zoomed-in crops (barely visible but common).

# Let's construct it as:
# 1. The long hollow tube.
# 2. A solid insert or base cap at the bottom if needed, but the image shows a continuous profile.
# It looks like a single extrusion that is hollow. The color difference is likely material/paint in the render.
# BUT, there is a faint line separating the black and grey.
# And there seems to be a small detail (bolt head/hole) on the black face.

# Revised Strategy:
# 1. Create the top tube (hollow).
# 2. Create the bottom base (solid or thick-walled).
# 3. Union them.

# Top Tube Parameters
top_section_height = total_height - base_height

# 1. Top Tube
top_tube = (
    cq.Workplane("XY")
    .workplane(offset=base_height) # Start on top of the base
    .rect(width, depth)
    .extrude(top_section_height)
    .faces(">Z").shell(-wall_thickness)
)

# 2. Bottom Base
# Assuming the base is also the same outer profile
base = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(base_height)
)

# Optional: Add the small detail on the bottom face (bolt/hole)
# There appears to be a small dot on the front face of the black section.
bolt_height = base_height / 2.0
bolt_radius = 3.0

base = (
    base.faces(">Y").workplane()
    .center(0, -base_height/2 + bolt_height) # centering vertically on the face relative to workplane center
    .circle(bolt_radius)
    .cutThruAll() 
)

# Combine them
result = base.union(top_tube)

# If the result needs to be a single "shell" everywhere (hollow base too):
# We would just extrude the whole thing and shell it.
# But the "black base" implies a separate component or assembly. 
# The code above creates a valid solid geometry representing the assembly.
