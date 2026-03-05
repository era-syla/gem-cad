import cadquery as cq

th = 4
plate_h = 80
plate_d = 50
spacing = 30
base_t = 6
tri_w = 10
tri_h = 12

# Side plate profile
side_pts = [
    (0, 0),
    (plate_d, 0),
    (plate_d, plate_h*0.9),
    (plate_d*0.8, plate_h),
    (0, plate_h),
]

# Create one side plate
plate1 = cq.Workplane("XZ").polyline(side_pts).close().extrude(th)

# Add round holes on front face
plate1 = plate1.faces(">Y").workplane().pushPoints(
    [(5, plate_h-10), (plate_d-5, plate_h-10)]
).circle(3).cutThruAll()

# Add triangular cutouts
tri_cuts = [
    [(5, 20), (5, 20+tri_h), (5+tri_w, 20+tri_h)],
    [(5, 40), (5, 40+tri_h), (5+tri_w, 40+tri_h)],
    [(5, 60), (5, 60+tri_h), (5+tri_w, 60+tri_h)],
]
wp = plate1.faces(">Y").workplane()
for tri in tri_cuts:
    wp = wp.polyline(tri).close().cutThruAll()
plate1 = wp

# Mirror second plate
plate2 = plate1.translate((0, spacing+th, 0))

# Combine plates
plates = plate1.union(plate2)

# Base
base = cq.Workplane("XY").rect(plate_d+10, spacing+2*th).extrude(base_t).translate((0, 0, -base_t))

# Front connector (simple rectangular brace)
y_center = (2*th + spacing)/2
connector = cq.Workplane("XY").workplane(offset=plate_h*0.6).center(plate_d-2.5, y_center).rect(5, spacing+2*th).extrude(th)

result = plates.union(base).union(connector)