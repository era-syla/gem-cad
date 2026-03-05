import cadquery as cq

# Parametric dimensions for the model
plate_radius = 100.0        # Radius of the main circular body
plate_thickness = 5.0       # Thickness of the plate
tab_width = 80.0            # Width of the rectangular tab
tab_extension = 40.0        # Length the tab protrudes from the circle edge
bolt_circle_radius = 90.0   # Radius of the hole pattern
num_holes = 16              # Number of holes in the pattern
hole_radius = 2.5           # Radius of the mounting holes

# 1. Create the main circular disc
disc = cq.Workplane("XY").circle(plate_radius).extrude(plate_thickness)

# 2. Create the rectangular tab
# The tab is positioned to protrude from the left side (-X) of the circle.
# To ensure a solid connection without gaps, the rectangle starts at the circle center (0,0)
# and extends outwards beyond the edge.
# Total length = plate_radius (internal overlap) + tab_extension (protrusion)
# Left edge x = -(plate_radius + tab_extension)
# Right edge x = 0
# Center x = -(plate_radius + tab_extension) / 2
rect_length = plate_radius + tab_extension
rect_center_x = -(plate_radius + tab_extension) / 2.0

tab = (
    cq.Workplane("XY")
    .center(rect_center_x, 0)
    .rect(rect_length, tab_width)
    .extrude(plate_thickness)
)

# 3. Union the disc and tab to create the base geometry
base_geo = disc.union(tab)

# 4. Create the pattern of holes
# We select the top face, create a polar array, and cut the holes
result = (
    base_geo.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_radius, 0, 360, num_holes)
    .circle(hole_radius)
    .cutThruAll()
)