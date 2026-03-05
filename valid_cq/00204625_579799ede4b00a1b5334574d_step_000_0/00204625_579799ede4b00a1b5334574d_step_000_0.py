import cadquery as cq

# Parametric dimensions for the model
base_size = 400.0       # Width and length of the square base plate
base_thickness = 10.0   # Thickness of the base plate
tube_od = 80.0          # Outer diameter of the central tube
tube_height = 180.0     # Height of the tube
tube_wall = 4.0         # Wall thickness of the tube

# Derived dimensions
tube_id = tube_od - (2 * tube_wall)

# Generate the geometry
result = (
    cq.Workplane("XY")
    # Create the square base plate centered at origin
    .box(base_size, base_size, base_thickness)
    
    # Select the top face of the plate to sketch the tube
    .faces(">Z")
    .workplane()
    
    # Draw the annulus (ring) profile for the tube
    .circle(tube_od / 2.0)
    .circle(tube_id / 2.0)
    
    # Extrude the tube upwards
    .extrude(tube_height)
    
    # Cut the hole through the base plate to make it hollow all the way through
    .faces("<Z")
    .workplane()
    .circle(tube_id / 2.0)
    .cutThruAll()
)