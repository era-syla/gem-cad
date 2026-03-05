import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_length = 50.0  # Length of the square base
base_width = 50.0   # Width of the square base
base_height = 20.0  # Height (thickness) of the base

# Cylinder dimensions
cylinder_radius = 15.0  # Outer radius of the vertical cylinder
cylinder_height = 40.0  # Height of the cylinder from the top of the base
hole_radius = 8.0       # Radius of the central through-hole

# --- Modeling ---

# 1. Create the rectangular base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Select the top face of the base
top_face = base.faces(">Z").workplane()

# 3. Create the cylinder on top of the base
# We draw a circle and extrude it upwards.
# Note: We use combine=True (default) to merge it with the base.
structure = top_face.circle(cylinder_radius).extrude(cylinder_height)

# 4. Create the through-hole
# We select the top face of the new cylinder, draw a smaller circle, 
# and cut through the entire object.
result = (structure.faces(">Z")
          .workplane()
          .circle(hole_radius)
          .cutThruAll())

# Alternative (single chain) approach:
# result = (cq.Workplane("XY")
#           .box(base_length, base_width, base_height)
#           .faces(">Z").workplane()
#           .circle(cylinder_radius).extrude(cylinder_height)
#           .faces(">Z").workplane()
#           .circle(hole_radius).cutThruAll())