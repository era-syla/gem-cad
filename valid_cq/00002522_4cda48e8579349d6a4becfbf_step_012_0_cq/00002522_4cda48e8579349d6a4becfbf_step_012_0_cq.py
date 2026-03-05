import cadquery as cq

# --- Parameter Definitions ---

# Plate dimensions
plate_length = 60.0
plate_width = 40.0
plate_thickness = 5.0

# Elliptical Hole dimensions (Plate)
ellipse_major = 25.0  # Length along the long axis
ellipse_minor = 10.0  # Length along the short axis
ellipse_spacing = 30.0 # Distance between centers

# Link Arm dimensions
link_center_dist = 40.0  # Distance between hole centers
link_end_radius = 8.0    # Radius of the rounded ends
link_thickness = 5.0
link_hole_radius = 4.0   # Radius of the holes in the link
link_bar_width = 8.0     # Width of the connecting bar

# --- Part 1: Rectangular Plate with Elliptical Holes ---

# Create the base rectangle
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the points for the elliptical holes
# We'll place them symmetrically along the X-axis
hole_locations = [(-ellipse_spacing / 2, 0), (ellipse_spacing / 2, 0)]

# Cut the elliptical holes
# CadQuery creates ellipses by specifying radius along X and Y axes.
# So we need half the major/minor lengths.
# Note: The ellipses in the image are oriented with the major axis along Y.
plate = (plate.faces(">Z").workplane()
         .pushPoints(hole_locations)
         .ellipse(ellipse_minor / 2, ellipse_major / 2) # (x_radius, y_radius)
         .cutThruAll())

# --- Part 2: Link Arm (Dog-bone shape) ---

# We will construct this separately and position it relative to the plate
# to match the image layout approximately.

# Create the base sketch for the link
link_sketch = (
    cq.Sketch()
    .rect(link_center_dist, link_bar_width) # The connecting bar
    .push([(-link_center_dist / 2, 0), (link_center_dist / 2, 0)])
    .circle(link_end_radius) # The rounded ends
    .clean() # Merge the shapes
)

# Extrude the link base
link = cq.Workplane("XY").placeSketch(link_sketch).extrude(link_thickness)

# Cut the holes in the ends
link = (link.faces(">Z").workplane()
        .pushPoints([(-link_center_dist / 2, 0), (link_center_dist / 2, 0)])
        .circle(link_hole_radius)
        .cutThruAll())

# Move the link to a position similar to the image (bottom right of the plate)
# Let's shift it by: X = +40, Y = -40
link = link.translate((40, -40, 0))

# --- Combine for Final Result ---

# Combine both solids into one compound object for the 'result' variable
result = plate.union(link)