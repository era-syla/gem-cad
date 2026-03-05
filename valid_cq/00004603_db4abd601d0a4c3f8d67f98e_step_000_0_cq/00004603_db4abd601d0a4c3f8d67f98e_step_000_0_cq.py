import cadquery as cq

# Parameters
base_size = 100.0  # Width and Length of the base
top_size = 60.0    # Width and Length of the top flat area
height = 15.0      # Total height
corner_radius = 5.0 # Radius of the corners at the top
dish_radius = 35.0 # Radius of the circular depression
dish_depth = 5.0   # Depth of the circular depression

# Create the base profile (a square)
base_sketch = (
    cq.Sketch()
    .rect(base_size, base_size)
)

# Create the top profile (a rounded square)
top_sketch = (
    cq.Sketch()
    .rect(top_size, top_size)
    .vertices()
    .fillet(corner_radius)
)

# Loft between the base and the top to create the main body
# We create a loft between a sketch on the XY plane and one offset by 'height'
result = (
    cq.Workplane("XY")
    .placeSketch(base_sketch, top_sketch.moved(cq.Location(cq.Vector(0, 0, height))))
    .loft()
)

# Add the circular depression (dish) on top
result = (
    result.faces(">Z")
    .workplane()
    .circle(dish_radius)
    .cutBlind(-dish_depth)
)

# Optional: Add fillets to the side edges for a smoother transition if desired, 
# but the image shows fairly sharp transitions on the diagonals. 
# However, the transition from side slope to top flat looks smooth in some interpretations, 
# but strictly looking at the image, it's a lofted square-to-rounded-square.

# The image shows distinctive sharp creases running from the base corners 
# towards the top corners. A standard loft from square to rounded square 
# achieves exactly this geometry.

# Export or display
# show_object(result)