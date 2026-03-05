import cadquery as cq

def create_main_body():
    return (
        cq.Workplane("XY")
        .rect(60, 120)
        .extrude(10)
        .faces(">Z")
        .workplane()
        .rect(40, 100)
        .extrude(40)
    )
    
def create_rod():
    return (
        cq.Workplane("XY")
        .circle(3)
        .extrude(100)
    )

def create_rack():
    return (
        cq.Workplane("XY")
        .rect(8, 100)
        .extrude(10)
    )

def create_bracket():
    return (
        cq.Workplane("XY")
        .rect(20, 60)
        .extrude(20)
        .faces(">Y")
        .workplane()
        .rect(20, 10)
        .cutBlind(-10)
    )

def create_wheel():
    return (
        cq.Workplane("XY")
        .circle(15)
        .extrude(10)
        .faces(">Z")
        .workplane()
        .circle(5)
        .cutBlind(-5)
    )

def create_pinion():
    return (
        cq.Workplane("XY")
        .circle(5)
        .extrude(20)
        .faces(">Z")
        .workplane()
        .circle(2)
        .cutBlind(-10)
    )

main_body = create_main_body()
rod = create_rod()
rack = create_rack()
bracket = create_bracket()
wheel = create_wheel()
pinion = create_pinion()

result = main_body.union(rod).union(rack).union(bracket).union(wheel).union(pinion)
