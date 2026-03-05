import cadquery as cq

# Define parameters for the box object
box_size = 10.0
fillet_radius = 1.0
wedge_width = 5.0

# Define parameters for the cylinder object
cyl_radius = 5.0
cyl_height = 15.0
separation_distance = 30.0 # Distance between the two objects

# --- Object 1: The Filleted Box with a Wedge ---

# Create the base box
box = cq.Workplane("XY").box(box_size, box_size, box_size)

# Apply fillets to vertical edges
box = box.edges("|Z").fillet(fillet_radius)
# Apply fillets to the top edges
box = box.faces(">Z").edges().fillet(fillet_radius)
# Apply fillets to the bottom edges
box = box.faces("<Z").edges().fillet(fillet_radius)

# Create the wedge attachment
# We'll create a right-angled triangle profile and extrude it
wedge = (cq.Workplane("YZ")
         .center(-box_size/2, -box_size/2) # Position relative to the box corner
         .lineTo(0, wedge_width)
         .lineTo(-wedge_width, 0)
         .close()
         .extrude(box_size) # Extrude along X
         )
# Center the wedge extrusion to match the box side
wedge = wedge.translate((-box_size/2, 0, 0)) # Move slightly to align if needed, depending on origin

# Combine box and wedge
part1 = box.union(wedge)

# --- Object 2: The Sliced Cylinder ---

# Create a base cylinder
cylinder = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)

# Create a cutting tool (a large box) to slice the cylinder in half
# We want to keep a semi-circle profile
cutter = (cq.Workplane("XY")
          .center(-cyl_radius, 0) # Position to cut half
          .box(cyl_radius*2, cyl_radius*4, cyl_height*2)
          )

# Cut the cylinder
part2 = cylinder.cut(cutter)

# Translate part2 to the right to separate them as shown in the image
part2 = part2.translate((separation_distance, 0, 0))

# --- Combine Final Assembly ---

# Create the final result containing both separate solids
result = part1.union(part2)

# Export or visualization steps would go here in a standard script, 
# but the prompt asks for the variable 'result'.