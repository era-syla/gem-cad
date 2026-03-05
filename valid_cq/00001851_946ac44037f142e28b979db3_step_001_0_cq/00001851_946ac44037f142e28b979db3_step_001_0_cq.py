import cadquery as cq

# Parametric dimensions
ball_diameter = 10.0
shaft_length = 50.0
shaft_diameter = 4.0
tip_chamfer_length = 1.0  # Length of the conical tip section
tip_flat_diameter = 1.0   # Diameter of the very end flat face

# Create the main assembly components
# 1. The Ball Head
# We create a sphere centered at the origin
ball = cq.Workplane("XY").sphere(ball_diameter / 2.0)

# 2. The Shaft
# We create a cylinder starting from the center of the sphere extending outwards.
# Alternatively, we can start it at the surface of the sphere, but boolean union handles overlap well.
# Let's extrude a circle from the center of the sphere along the Z axis.
shaft = (cq.Workplane("XY")
         .circle(shaft_diameter / 2.0)
         .extrude(shaft_length)
         )

# 3. The Tip Detail
# The image shows a tapered end. We can achieve this by adding a cone at the end of the shaft.
# The cone base matches the shaft, top matches the flat tip diameter.
tip = (cq.Workplane("XY")
       .workplane(offset=shaft_length)
       .circle(shaft_diameter / 2.0)
       .workplane(offset=tip_chamfer_length)
       .circle(tip_flat_diameter / 2.0)
       .loft(combine=True)
       )

# Combine the parts
# Since the shaft and tip were built sequentially or could be separate, let's ensure they are all one solid.
# The 'ball' is separate currently.
# The 'shaft' variable actually creates a separate object in this script flow unless chained properly.
# Let's reconstruct cleanly in a single chain or union operation.

# Robust Construction Strategy:
# 1. Create Ball
# 2. Union with Shaft
# 3. Add Tip (or chamfer end)

final_part = ball.union(shaft)

# Create the tapered tip separately and union it
tip_solid = (cq.Workplane("XY")
             .workplane(offset=shaft_length)
             .circle(shaft_diameter / 2.0)
             .workplane(offset=tip_chamfer_length)
             .circle(tip_flat_diameter / 2.0)
             .loft()
             )

result = final_part.union(tip_solid)

# Export or display is handled by the user's environment, 
# but 'result' is the required variable.