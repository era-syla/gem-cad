import cadquery as cq

def create_model():
    # Define dimensions
    length = 100
    width = 20
    thickness = 5
    radius = 10
    
    # Create a rectangular base with rounded ends
    base = (cq.Workplane("XY")
            .moveTo(-length/2 + radius, 0)
            .lineTo(length/2 - radius, 0)
            .threePointArc((length/2, width/2), (length/2 - radius, width))
            .lineTo(-length/2 + radius, width)
            .threePointArc((-length/2, width/2), (-length/2 + radius, 0))
            .close()
            .extrude(thickness))
    
    # Add text
    text = (cq.Workplane("XY")
            .workplane(offset=thickness/2)
            .center(0, width/4)
            .text("FRAISEUR", 15, thickness, combine=False))
    
    # Cut the text out of the base
    result = base.cut(text)
    
    return result

result = create_model()