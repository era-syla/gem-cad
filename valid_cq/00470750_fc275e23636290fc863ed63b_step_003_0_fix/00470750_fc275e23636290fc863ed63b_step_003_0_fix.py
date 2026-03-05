import cadquery as cq

# Parameters
length = 80
width = 20
thickness = 5
hole_large_dia = 10
hole_small_dia = 5
rect_cut_length = 30
rect_cut_width = 12

# Base plate: center rectangle
center_rect = cq.Workplane("XY").rect(length - width, width).extrude(thickness)
# Semicircular ends
end_circle = cq.Workplane("XY").circle(width / 2).extrude(thickness)
end1 = end_circle.translate(( length/2 - width/2, 0, 0))
end2 = end_circle.translate((-length/2 + width/2, 0, 0))
plate = center_rect.union(end1).union(end2)

# Add holes and cutout on top face
result = (
    plate
    .faces(">Z")
    .workplane()
    # Large hole at one rounded end
    .center(length/2 - width/2, 0)
    .hole(hole_large_dia)
    # Small hole at other rounded end
    .workplane(offset=0)
    .center(- (length/2 - width/2), 0)
    .hole(hole_small_dia)
    # Rectangular cutout at center
    .workplane(offset=0)
    .center(0, 0)
    .rect(rect_cut_length, rect_cut_width)
    .cutThruAll()
)