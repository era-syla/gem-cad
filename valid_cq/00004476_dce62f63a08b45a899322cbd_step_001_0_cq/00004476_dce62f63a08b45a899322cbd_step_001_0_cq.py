import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Overall diameter of the tray
wall_thickness = 2.0    # Thickness of the side walls
base_thickness = 2.0    # Thickness of the bottom base
total_height = 8.0      # Total height of the tray including the rim
lip_step_height = 2.0   # Height of the small step on the outer bottom edge
lip_step_width = 1.0    # Width of the step indent

# Derived dimensions
inner_diameter = outer_diameter - (2 * wall_thickness)
inner_height = total_height - base_thickness

# Create the main body
# Start with the outer cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(total_height)

# Create the inner cavity (pocket)
# We subtract a cylinder from the top face
result = result.faces(">Z").workplane().circle(inner_diameter / 2).cutBlind(-inner_height)

# Create the subtle step/lip on the bottom outer edge
# This is often seen on lids to help them stack or seal
# We select the bottom edge and chamfer or cut a profile. 
# Looking at the image, it looks like a small revolved cut or a second cylinder at the base.
# Let's model it as a slight reduction in diameter at the very bottom section, or a step.
# Based on the image, there is a visible line on the outer wall near the bottom.
# Let's make the main extrusion the full diameter, then cut a small step at the bottom.

# Alternative approach for cleaner geometry: Revolve a profile.
# Profile points:
# 1. Start at origin (0,0)
# 2. Go out to inner radius (inner_diameter/2, 0)
# 3. Go up to inner thickness (inner_diameter/2, base_thickness)
# 4. Go out to outer radius (outer_diameter/2, base_thickness) - but wait, the wall goes all the way up.

# Let's stick to the CSG approach as it's often easier to read.
# We have the cup shape. Now let's add the detail on the outside.
# The image shows a small step near the bottom of the outer wall.
# Let's cut a ring from the bottom outer edge.

# Select the bottom face, draw a large circle (larger than object) and a circle for the step cut
cut_outer_r = outer_diameter / 2 + 10 # Arbitrary large number
cut_inner_r = (outer_diameter / 2) - lip_step_width

# Perform the cut at the bottom
result = result.faces("<Z").workplane().circle(cut_outer_r).circle(cut_inner_r).cutBlind(lip_step_height)

# Fillets
# The image shows smooth edges.
# Fillet the top rim
try:
    result = result.edges(">Z").fillet(wall_thickness / 3.0)
except:
    pass # In case fillet fails due to geometry complexity

# Fillet the inner bottom edge
try:
    result = result.faces(">Z[-2]").edges("%Circle").fillet(wall_thickness / 2.0)
except:
    pass

# Fillet the outer bottom edge where the step is
try:
    # Select edges at the bottom
    result = result.edges("<Z").fillet(0.5)
except:
    pass

# The variable 'result' now contains the final geometry