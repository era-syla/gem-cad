import cadquery as cq

# Define the path for the handle
path = cq.Workplane("XZ").moveTo(0, 10).threePointArc((10, 15), (20, 10)).lineTo(30, 10)

# Create the profile for the handle
profile = cq.Workplane("YZ").center(0, 10).rect(5, 5)

# Sweep the profile along the path
result = profile.sweep(path)

# Check the result
if not result.val().isValid():
    raise ValueError("The result is not a valid solid.")