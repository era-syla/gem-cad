import cadquery as cq

# Parametric dimensions based on visual estimation
head_diameter = 30.0     # Diameter of the large head
head_length = 15.0       # Axial length of the head
shaft_diameter = 16.0    # Diameter of the shaft
shaft_length = 50.0      # Axial length of the shaft
neck_fillet = 2.5        # Radius of the fillet between head and shaft
end_chamfer = 1.5        # Chamfer distance at the end of the shaft

# 1. Create the head cylinder
# Start on the XY plane and extrude the main head geometry
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_length)

# 2. Create the shaft cylinder
# Select the top face of the head (max Z), create a new workplane, and extrude the shaft
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Apply fillet at the neck (intersection of head and shaft)
# We select the edge by finding the one nearest to the theoretical circle on the step
# Point: (Radius of shaft, 0, Height of head)
neck_selector = cq.NearestToPointSelector((shaft_diameter / 2.0, 0, head_length))
result = result.edges(neck_selector).fillet(neck_fillet)

# 4. Apply chamfer to the end of the shaft
# Select the circular edge at the extreme positive Z direction
result = result.edges(">Z").chamfer(end_chamfer)