import cadquery as cq

# =============================================================================
# Parametric Dimensions
# =============================================================================
length = 90.0        # Total length of the link
width = 30.0         # Width of the main body
height = 30.0        # Height of the main body
hole_diameter = 10.0 # Diameter of the thru-holes
slot_width = 12.0    # Gap size of the clevis slots
slot_depth = 22.0    # Depth of the slots into the body

# Derived radii for fully rounded ends
# We subtract a tiny epsilon to ensure stable kernel operations during fillets
fillet_radius_left = width / 2.0 - 0.001
fillet_radius_right = height / 2.0 - 0.001

# =============================================================================
# Model Generation
# =============================================================================

# 1. Base Block
# Create the central rectangular prism centered at origin
result = cq.Workplane("XY").box(length, width, height)

# -----------------------------------------------------------------------------
# 2. Left End (XY Plane Clevis)
# Features: Rounded in XY plane, Vertical Hole (Z-axis), Horizontal Slot
# -----------------------------------------------------------------------------

# A. Round the end
# Select vertical edges (|Z) at the minimum X face (<X)
result = result.edges("<X and |Z").fillet(fillet_radius_left)

# B. Cut the horizontal slot
# Create a workplane on the left face (<X)
# Draw a rectangle that defines the gap height (Z dimension) and spans full width
# Cut inwards (negative direction relative to face normal)
result = (result.faces("<X").workplane()
          .rect(width * 2, slot_width)
          .cutBlind(-slot_depth))

# C. Drill the vertical hole
# Select the top face (>Z)
# Move center to the arc center of the rounded end
# Hole goes through the entire part in Z
center_x_left = -length/2.0 + (width / 2.0)
result = (result.faces(">Z").workplane()
          .center(center_x_left, 0)
          .hole(hole_diameter))

# -----------------------------------------------------------------------------
# 3. Right End (XZ Plane Clevis - Rotated 90 degrees)
# Features: Rounded in XZ plane, Horizontal Hole (Y-axis), Vertical Slot
# -----------------------------------------------------------------------------

# A. Round the end
# Select horizontal edges parallel to Y (|Y) at the maximum X face (>X)
result = result.edges(">X and |Y").fillet(fillet_radius_right)

# B. Cut the vertical slot
# Create a workplane on the right face (>X)
# Draw a rectangle that defines the gap width (Y dimension) and spans full height
result = (result.faces(">X").workplane()
          .rect(slot_width, height * 2)
          .cutBlind(-slot_depth))

# C. Drill the horizontal hole
# Select the side face (>Y)
# Move center to the arc center of the rounded end
# Note: On >Y face, local coordinates are mapped such that hole() drills along Y
center_x_right = length/2.0 - (height / 2.0)
result = (result.faces(">Y").workplane()
          .center(center_x_right, 0)
          .hole(hole_diameter))

# The 'result' variable now contains the final geometry