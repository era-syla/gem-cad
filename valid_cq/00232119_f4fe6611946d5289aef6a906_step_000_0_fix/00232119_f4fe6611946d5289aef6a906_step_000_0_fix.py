import cadquery as cq

# Create a 2D profile with splines and lines
profile = (cq.Workplane("XY")
           .moveTo(0, 0)
           .lineTo(0, 10)
           .threePointArc((5, 15), (10, 10))
           .threePointArc((15, 5), (20, 10))
           .lineTo(20, 0)
           .close())

# Extrude the profile to create a 3D shape
result = profile.extrude(3)