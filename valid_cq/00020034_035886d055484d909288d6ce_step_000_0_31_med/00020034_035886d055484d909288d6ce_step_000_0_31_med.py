import cadquery as cq

# Parameters
length = 100.0
height = 20.0
width = 15.0
web_thickness = 5.0
flange_thickness = 10.0
tab_extension = 5.0
tab_width = 10.0
tab_thickness = 5.0
hole_diameter = 4.0
tab_locations = [20.0, 80.0]

# Create the main profile
profile_points = [
    (0, 0),
    (0, height),
    (width, height),
    (width, height - flange_thickness),
    (web_thickness, height - flange_thickness),
    (web_thickness, 0)
]

# Base L-bracket body
result = cq.Workplane("XZ").polyline(profile_points).close().extrude(length)

# Add rear tabs
for y_pos in tab_locations:
    tab = cq.Workplane("XY").transformed(
        offset=(-tab_extension / 2.0, y_pos, height - tab_thickness / 2.0)
    ).box(tab_extension, tab_width, tab_thickness)
    result = result.union(tab)

# Cut clearance holes in the lower web
web_height = height - flange_thickness
hole_z_pos = web_height / 2.0

holes_tool = (
    cq.Workplane("YZ")
    .workplane(offset=-10.0) 
    .pushPoints([(y, hole_z_pos) for y in tab_locations])
    .circle(hole_diameter / 2.0)
    .extrude(30.0) 
)

result = result.cut(holes_tool)