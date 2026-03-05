import cadquery as cq

# Parametric dimensions
# The image shows a very thin, long rod or tube.
length = 100.0  # Total length of the rod
diameter = 1.0  # Diameter of the rod (thin relative to length)
end_cap_length = 2.0  # Length of the distinct end sections visible in the image

# Create the main rod body
# We'll create a cylinder centered on the Z axis
rod = cq.Workplane("XY").circle(diameter / 2).extrude(length)

# Optional: Add detail for the "end caps" if they are distinct features.
# In the image, the ends look slightly different, possibly just rendering artifacts 
# or indicating a chamfer/fillet. Let's add a small chamfer to both ends to represent this.
result = rod.faces("<Z or >Z").chamfer(diameter * 0.1)

# Alternatively, if the image implies a tube (hollow rod):
# result = cq.Workplane("XY").circle(diameter / 2).circle((diameter / 2) - 0.2).extrude(length)
# But a solid rod is the safest interpretation of a simple line.

# Export or display the result
# show_object(result)