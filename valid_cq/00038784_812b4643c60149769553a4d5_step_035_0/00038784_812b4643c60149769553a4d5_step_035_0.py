import cadquery as cq

# Define parametric dimensions based on visual estimation of the slender rod
rod_length = 200.0
rod_diameter = 4.0
rod_radius = rod_diameter / 2.0

# Create the cylindrical rod geometry
# Start on the XY plane, draw the circular profile, and extrude vertically
result = cq.Workplane("XY").circle(rod_radius).extrude(rod_length)