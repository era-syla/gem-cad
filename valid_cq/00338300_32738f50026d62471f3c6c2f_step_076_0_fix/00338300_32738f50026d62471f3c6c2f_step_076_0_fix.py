import cadquery as cq

# Define dimensions
length = 150.0
width = 20.0
thickness = 2.0
hole_diameter = 3.0
num_teeth = 15
tooth_depth = 1.0
end_radius = 10.0

# Create the main body
base = cq.Workplane("XY").moveTo(-length/2 + end_radius, 0)\
    .lineTo(length/2 - end_radius, 0)\
    .threePointArc((length/2, width/2), (length/2 - end_radius, width))\
    .lineTo(-length/2 + end_radius, width)\
    .threePointArc((-length/2, width/2), (-length/2 + end_radius, 0))\
    .close().extrude(thickness)

# Create teeth pattern on the edge
tooth_spacing = (length - 2 * end_radius) / (num_teeth + 1)
teeth_profile = cq.Workplane("XY").polyline([
    (0, 0), 
    (tooth_spacing / 2, -tooth_depth), 
    (tooth_spacing, 0)
]).close().revolve(angleDegrees=360)

teeth = base.faces(">Z").workplane(centerOption="CenterOfBoundBox")\
    .rarray(tooth_spacing, 1, num_teeth, 1).add(teeth_profile)

# Combine teeth with base
body_with_teeth = base.union(teeth)

# Add holes
hole_positions = [(0, 0), (-length/4, 0), (length/4, 0), (-length/2 + end_radius, 0), (length/2 - end_radius, 0)]
holes = body_with_teeth.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)

# Final result
result = holes