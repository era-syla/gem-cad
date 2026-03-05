import cadquery as cq

# Define dimensions based on the visual approximation
# The object looks like a thin, long bar with angled ends.
length = 100.0  # Overall length
width = 10.0    # Width of the bar
thickness = 5.0 # Thickness of the bar
angle = 45.0    # Angle of the cut ends (looks roughly 45 degrees)

# Create the base shape
# We can start with a rectangular box and then cut the ends, 
# or sketch the profile and extrude. Sketching is often cleaner for angled ends.

# Method: Sketching the trapezoidal profile on the XY plane and extruding in Z.
# Let's visualize the profile from the "top" (though the image is isometric).
# It's a parallelogram if viewed from the side, or a trapezoid depending on the cut direction.
# Looking at the image, it looks like a parallelepiped (a sheared box) or a bar with mitered ends.
# Let's assume it's a bar where the ends are cut parallel to each other (parallelogram profile).

# Calculate the offset needed for the angle
import math
offset = width / math.tan(math.radians(angle))

# Let's construct it using a sketch for the parallelogram profile
# Coordinates for the points of the parallelogram
# (0,0) -> (length, 0) -> (length - offset, width) -> (-offset, width) -> close
# This creates a parallelogram shape.

pts = [
    (0, 0),
    (length, 0),
    (length - offset, width),
    (-offset, width)
]

# Create the workplane and the extrusion
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Alternatively, just modeling a box and lofting or shearing might work, 
# but defining points is explicit and robust.
# Let's re-examine the image carefully.
# It looks like a long rectangular strip that has been cut at an angle at both ends.
# The cuts appear parallel.
# Let's adjust the points to center it roughly or keep it simple.

# A simpler parametric approach:
# Create a box, then slice it. Or extrude a sketch.
# Let's stick to the sketch approach as it's very readable.

# Refined Dimensions to match aspect ratio of image better
length = 150.0
width = 20.0
thickness = 5.0
skew_offset = 20.0 # This controls the angle directly without trig

pts = [
    (0, 0),
    (length, 0),
    (length + skew_offset, width),
    (skew_offset, width)
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)