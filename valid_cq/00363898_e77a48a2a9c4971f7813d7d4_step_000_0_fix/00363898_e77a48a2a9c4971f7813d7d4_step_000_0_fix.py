import cadquery as cq

length = 100.0
width = 20.0
base_thickness = 5.0
fin_count = 4
fin_thickness = 1.0
fin_height = 3.0

spacing = (width - fin_count * fin_thickness) / (fin_count + 1)
y_positions = [
    -width/2 + spacing*(i+1) + fin_thickness*i + fin_thickness/2
    for i in range(fin_count)
]
pts = [(0, y) for y in y_positions]

result = cq.Workplane("XY").box(length, width, base_thickness)
result = result.faces(">Z").workplane().pushPoints(pts).rect(length, fin_thickness).extrude(fin_height)
result = result.faces("<Z").workplane().pushPoints(pts).rect(length, fin_thickness).extrude(-fin_height)