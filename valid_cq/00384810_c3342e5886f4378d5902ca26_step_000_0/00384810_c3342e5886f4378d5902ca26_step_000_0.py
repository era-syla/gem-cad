import cadquery as cq

# Geometric Parameters
total_length = 500.0    # Total length of the shaft
main_diameter = 12.0    # Diameter of the central section
end_diameter = 8.0      # Diameter of the reduced ends
end_length = 20.0       # Length of the reduced section at each end
tip_chamfer = 1.0       # Chamfer dimension at the tips

# Calculate the length of the thick central section
# The total length comprises the center section plus two end sections
center_length = total_length - (2 * end_length)

# 1. Create the main central cylinder
# We extrude symmetrically from the XY plane to keep the origin at the center
result = cq.Workplane("XY").circle(main_diameter / 2.0).extrude(center_length / 2.0, both=True)

# 2. Add the reduced diameter step to the positive Z end
result = (
    result.faces(">Z")
    .workplane()
    .circle(end_diameter / 2.0)
    .extrude(end_length)
)

# 3. Add the reduced diameter step to the negative Z end
# The workplane on the <Z face has a normal pointing in -Z, so extrude adds material outwards
result = (
    result.faces("<Z")
    .workplane()
    .circle(end_diameter / 2.0)
    .extrude(end_length)
)

# 4. Add chamfers to the outer edges of both tips for a finished look
# Select the faces at the extreme Z limits and chamfer their edges
result = result.faces(">Z or <Z").edges().chamfer(tip_chamfer)