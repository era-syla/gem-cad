import cadquery as cq

# Parametric dimensions
diameter = 50.0      # Overall diameter of the object
thickness = 10.0     # Total thickness (height)
fillet_radius = 4.0  # Radius of the rounded edge
groove_width = 0.2   # Width of the visible seam lines

# 1. Create the main body: a cylinder with rounded edges
# We start with a cylinder
base = cq.Workplane("XY").cylinder(thickness, diameter / 2)

# Apply a fillet to the top and bottom edges to create the rounded "puck" shape
# The image shows a very significant rounding, almost like a torus section on the outside.
# Let's fillet both the top and bottom edges.
result = base.edges().fillet(fillet_radius)

# 2. Create the circular groove on top
# The image shows a circular line on the top face. This is likely a parting line or a separate insert.
# We will model this as a thin, shallow circular groove.
# The groove is inset from the edge, roughly where the fillet ends.
groove_diameter = diameter - (2 * fillet_radius) - 2.0 

# Create a tool to cut the circular groove
circular_groove = (
    cq.Workplane("XY")
    .workplane(offset=thickness/2) # Move to the top face
    .circle(groove_diameter / 2)
    .circle((groove_diameter / 2) - groove_width)
    .extrude(-0.2) # Very shallow cut
)

result = result.cut(circular_groove)

# 3. Create the vertical seam
# The image shows a vertical line running down the side. This looks like a mold parting line
# or an assembly seam.
# We create a thin box to cut this slit/groove.
seam_depth = 0.2
seam_tool = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 0, 45)) # Rotate to match the angle in the image roughly
    .box(diameter + 5, groove_width, thickness + 2) # Make it large enough to cut through
)

# We only want the seam on the side surface, not cutting deep into the object.
# A more robust way to make a "surface seam" is to make a shell slightly larger, 
# intersection it, or just use a boolean cut with a specific shape. 
# However, for a visual match, a simple cut is often sufficient if kept shallow.
# Let's make a ring tool that represents the outer surface and cut a slot into it, 
# then subtract that "embossment" from the main body? No, that's overcomplicating.

# Let's just cut a radial slot.
# To make it look like the image (a line on the surface), a very thin cut works best.
# We want it only on one side as per the image view, but usually these are symmetric.
# The image shows it specifically on the curved surface.

# Let's create a cutting tool that is a thin rectangular solid, but positioned 
# so it only nicks the surface.
seam_cutter = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(rotate=(0, 0, -135)) # Position the seam visually
    .moveTo(diameter/2 - 0.5, 0)      # Move to the edge
    .rect(5, groove_width)            # A rectangle cutting into the edge
    .extrude(thickness, both=True)    # Extrude vertically
)

# We need to limit this cut so it doesn't slice the whole way through the flat top unnecessarily deep,
# although the image shows the seam connecting to the circular groove.
# Let's apply the cut.
result = result.cut(seam_cutter)

# Optional: Refine the circular groove to ensure it's clean
# (The boolean operations above should be sufficient)

# Final result is stored in 'result' variable