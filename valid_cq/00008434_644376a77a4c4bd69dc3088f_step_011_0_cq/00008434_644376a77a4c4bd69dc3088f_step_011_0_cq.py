import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the rod
diameter = 5.0   # Diameter of the rod

# Create the cylindrical rod
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)

# Optional: If you wanted to center it, you could do:
# result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length, both=True)

# Export or display
if "show_object" in locals():
    show_object(result)