import cadquery as cq

# Parametric dimensions
length = 120.0
width = 60.0
height = 50.0

# Profile points for the decorative molding cross-section
# Approximating the complex curved sides and stepped top
profile_pts = [
    (10, 0),
    (width - 10, 0),
    (width - 10, 5),
    (width - 15, 10),
    (width - 15, 25),
    (width, 35),
    (width, 40),
    (width - 5, 43),
    (width - 2, 47),
    (width - 10, height),
    (10, height),
    (2, 47),
    (5, 43),
    (0, 40),
    (0, 35),
    (15, 25),
    (15, 10),
    (10, 5)
]

# Create the main extruded body
result = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(length)
)

# Apply fillets to longitudinal edges to soften the profile
# This mimics the smooth, sweeping curves seen in the molding
try:
    result = result.edges("%X").fillet(1.5)
except:
    pass # Fallback in case geometry prevents uniform filleting

# Add the raised flat section on the very top
result = (
    result.faces(">Z")
    .workplane()
    .rect(length, width - 25)
    .extrude(2.5)
)

# Add indentations/cutouts to represent the irregular, broken-looking sections 
# observed on the top right edge of the model
result = (
    result.faces(">X")
    .workplane(offset=-5)
    .center(0, 15)
    .pushPoints([(-15, 0), (-5, 5), (8, 2)])
    .rect(3.5, 18)
    .cutBlind(-25)
)

# Add another small subtractive feature on the lower side
result = (
    result.faces("<X")
    .workplane(offset=-10)
    .center(-20, -15)
    .circle(4)
    .cutBlind(-15)
)