import cadquery as cq
import math

# Create a cylindrical base/stem
stem = cq.Workplane("XY").circle(15).extrude(30)

# Create the curved wing/flap shape on top
# The wing is a curved surface that looks like a saddle or curved plate
# We'll create it using a loft between two curves at different heights

# Create the wing as a thin solid using loft
# The wing spans wide in X direction and curves up

# Make the wing using a series of profiles
# Bottom profile at the top of stem (z=30)
# The wing curves up from center and droops at edges

# Let's create the wing as an extruded and bent shape
# Using shell approach: create a box and apply transformations

# Create wing base shape - a curved plate
# We'll approximate the curved wing with a solid built from spline

# Wing dimensions
wing_length = 120  # X direction
wing_width = 80    # Y direction
wing_thickness = 3

# Create the wing as a flat plate first, then we'll work with it
# The wing appears to be a curved saddle shape

# Build wing using loft with multiple cross-sections
# Front edge (high), back edge curves down at sides

# Create wing using workplane and spline approximation
# The shape looks like a curved rectangular plate with curved edges

# Let's create the wing by extruding a profile and using shell
# Approximate with a swept/lofted solid

# Create bottom wire of wing at z=30 (top of stem)
p1 = cq.Workplane("XY").workplane(offset=30)

# Build the wing as a solid by creating top and bottom faces
# Use a simple approach: create a box and apply transformations

# Wing: curved surface approximated by a solid
# Create multiple horizontal cross sections and loft them

# Profile 1 at y = -40 (back), z=30 (low)
# Profile 2 at y = 0 (middle), z=50 (high)  
# Profile 3 at y = 40 (front), z=30 (low)

# Create the wing using a series of rectangular profiles
def make_wing():
    # Create profiles at different y positions
    profiles = []
    
    # Build the wing solid using boolean operations
    # Start with a curved shape
    
    # Create a solid wing by sweeping
    # Use loft with wires
    
    w = cq.Workplane("XZ")
    
    # Create cross-section profiles along Y axis
    result = cq.Workplane("XY")
    
    # Create the curved wing shape
    # Profile at y=-40: narrow, low
    # Profile at y=0: wide, high  
    # Profile at y=40: narrow, low
    
    pts_bottom = [(-50, -40, 28), (0, -40, 28), (50, -40, 28)]
    pts_mid = [(-60, 0, 45), (0, 0, 50), (60, 0, 45)]
    pts_top_edge = [(-40, 40, 28), (0, 40, 28), (40, 40, 28)]
    
    wire1 = cq.Workplane("XY").workplane(offset=28).moveTo(-50, -40).lineTo(50, -40).val()
    wire2 = cq.Workplane("XY").workplane(offset=50).moveTo(-60, 0).lineTo(60, 0).val()
    wire3 = cq.Workplane("XY").workplane(offset=28).moveTo(-40, 40).lineTo(40, 40).val()
    
    return None

# Better approach: create wing as a thick curved surface
# Use a box and carve it

# Create a large curved wing body
wing = (cq.Workplane("XY")
        .workplane(offset=25)
        .rect(130, 90)
        .workplane(offset=30)
        .rect(140, 95)
        .loft()
        )

# Cut the bottom to create curve
# Cut sides to taper
cutter_left = cq.Workplane("XY").workplane(offset=0).rect(200, 200).extrude(60)
cutter_left = cq.CQ(cutter_left.val()).translate((-90, 0, 0))

# Create the curved wing using shell on a cylinder-intersected box
wing2 = (cq.Workplane("XY")
         .workplane(offset=28)
         .rect(140, 90)
         .extrude(8)
         )

# Combine stem and wing
result = stem.union(wing2)

# Add a raised profile on the wing (the teardrop/egg shape visible on top)
teardrop = (cq.Workplane("XY")
            .workplane(offset=36)
            .ellipse(12, 15)
            .extrude(2)
            )

result = result.union(teardrop)