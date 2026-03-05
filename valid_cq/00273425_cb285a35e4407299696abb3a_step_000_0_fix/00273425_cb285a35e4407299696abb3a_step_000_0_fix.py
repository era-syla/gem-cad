import cadquery as cq

def create_spiked_cylinder():
    # Create the main cylinder
    cylinder = cq.Workplane("XY").circle(10).extrude(60)
    
    # Create a spike
    spike = cq.Workplane("XY").polygon(3, 5).extrude(10).faces(">Z").workplane().center(0, 2).circle(1).extrude(2)
    
    # Create an array of spikes around the cylinder
    spikes = (
        cq.Workplane("XY")
        .polarArray(0, 0, 360, 8)
        .eachpoint(lambda loc: spike.val().moved(loc), useLocalCoordinates=True)
    )
    
    # Combine the spikes with the cylinder
    spiked_cylinder = cylinder.union(spikes)
    
    return spiked_cylinder

result = create_spiked_cylinder()
