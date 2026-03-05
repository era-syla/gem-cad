import cadquery as cq
import math

# --- Parametric Dimensions ---
# Main ring dimensions
outer_diameter = 150.0
inner_diameter = 100.0
thickness = 25.0

# Inner step/shoulder dimensions
inner_shoulder_diameter = 110.0  # Slightly larger than inner_diameter
inner_shoulder_depth = 8.0       # How deep the wider cut goes from the back (or front)

# Tab/Protrusion dimensions
tab_width = 40.0         # Approximate width of the raised section
tab_extra_radius = 5.0   # How much further out the tab goes than the OD
tab_start_angle = 70.0   # Angle span in degrees (visual estimation)
tab_chamfer = 2.0        # Chamfer on the tab edges if needed (looks fairly sharp but clean)

# Bolt hole pattern dimensions
bolt_circle_diameter = 130.0
num_holes = 16
hole_diameter = 6.0

# --- Modeling ---

# 1. Base Ring
# Create the main cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)

# 2. Add the Tab/Protrusion on top
# We need a shape that follows the outer curvature but extends further out.
# One way is to make a sector or a larger circle and intersect/cut.
# Let's make a larger cylinder sector.
tab_radius = (outer_diameter / 2) + tab_extra_radius

# Calculate points for a polygon that represents the tab shape
# We want it centered on the Y-axis (top) for symmetry
angle_half = tab_start_angle / 2.0
rad_angle = math.radians(angle_half)

# We construct a wedge-like shape to add to the top
tab_shape = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(tab_radius * math.sin(rad_angle), tab_radius * math.cos(rad_angle))
    .radiusArc((-tab_radius * math.sin(rad_angle), tab_radius * math.cos(rad_angle)), tab_radius)
    .close()
    .extrude(thickness)
)

# Intersect this wedge with a rectangular block to define the flat sides if it's rectangular,
# or just use the wedge if it's purely radial. 
# Looking at the image, the sides of the tab are parallel (vertical cuts), 
# not radial lines. It looks like a rectangular block merged with the cylinder.
# Let's adjust approach: Create a rectangle and intersect with a larger cylinder?
# Or simply extrude a rectangle and cut away the excess?

# Revised Tab approach: A rectangular extrusion centered on Y, width = tab_width
tab_rect = (
    cq.Workplane("XY")
    .center(0, outer_diameter/2) # Move to the edge
    .rect(tab_width, tab_extra_radius * 4) # Make it tall enough
    .extrude(thickness)
)

# We need the outer curvature of the tab.
# Let's make a large cylinder representing the max extent of the tab
outer_limit = cq.Workplane("XY").circle(outer_diameter/2 + tab_extra_radius).extrude(thickness)

# Intersect the rectangle with the outer limit cylinder to get the curved top
tab_final = tab_rect.intersect(outer_limit)

# Fuse the tab to the base ring
body = base.union(tab_final)

# 3. Create the Main Center Hole
# Cut through the entire thickness
body = body.faces(">Z").workplane().hole(inner_diameter)

# 4. Create the Inner Shoulder/Counterbore
# Cut from one side (assuming back side based on typical bearing housing design, 
# or front depending on orientation, let's cut from >Z for visibility)
body = body.faces(">Z").workplane().circle(inner_shoulder_diameter / 2).cutBlind(-inner_shoulder_depth)

# 5. Bolt Hole Pattern
# Select the face, create a circle for reference (conceptually), and place holes
body = (
    body.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_diameter / 2, 0, 360, num_holes)
    .circle(hole_diameter / 2)
    .cutBlind(-thickness)
)

# 6. Refinement: The Cutout/Keyway on the Tab
# The image shows the tab isn't a solid block; it has a rectangular profile 
# but sits *on top* of the ring. However, looking closer at the intersection,
# the tab has sharp vertical walls.
# The previous boolean operation (union) handled the shape correctly.
# There appear to be small steps or "reliefs" where the tab meets the main circle 
# in the image, but the provided code approximates the "rectangular protrusion with curved top" 
# which is the dominant feature.

result = body