import cadquery as cq

# Parameters for the Blind Flange
flange_diameter = 150.0  # Overall diameter of the flange
flange_thickness = 15.0  # Thickness of the flange
bolt_circle_diameter = 120.0  # Diameter of the circle on which holes are placed
num_holes = 8  # Number of bolt holes
hole_diameter = 10.0  # Diameter of the bolt holes

# Create the base disc
result = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# Create the bolt hole pattern
# We select the top face, push points for the hole locations, and cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(
        radius=bolt_circle_diameter / 2, 
        startAngle=0, 
        angle=360, 
        count=num_holes
    )
    .circle(hole_diameter / 2)
    .cutThruAll()
)