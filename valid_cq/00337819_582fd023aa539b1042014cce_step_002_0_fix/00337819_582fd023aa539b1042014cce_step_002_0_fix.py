import cadquery as cq

text_content = "PERRINN\nWe are a Team"
result = cq.Workplane("XY").text(text_content, 10, 1, combine=True)