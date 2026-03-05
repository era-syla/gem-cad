import cadquery as cq

# Parameters
beam_length = 150
beam_width = 20
crossbar_depth = 20
crossbar_width = 60
thickness = 10
gusset_height = 5
hole_dia = 6
hole_offset = 10

# Base T-shaped extrusion
base = (
    cq.Workplane("XY")
    .polyline([
        (-beam_width/2, -beam_length),
        ( beam_width/2, -beam_length),
        ( beam_width/2, 0),
        ( crossbar_width/2, 0),
        ( crossbar_width/2, crossbar_depth),
        (-crossbar_width/2, crossbar_depth),
        (-crossbar_width/2, 0),
        (-beam_width/2, 0),
    ])
    .close()
    .extrude(thickness)
)

# Triangular gusset under the crossbar (extruded along Y)
gusset = (
    cq.Workplane("XZ", origin=(0, crossbar_depth/2, 0))
    .polyline([
        (-beam_width/2, 0),
        ( beam_width/2, 0),
        ( 0, gusset_height),
    ])
    .close()
    .extrude(crossbar_depth, combine=True)
)

# Combine base and gusset
combined = base.union(gusset)

# Drill two holes through the crossbar
result = (
    combined
    .faces(">Z")                      # top face
    .workplane()
    .pushPoints([
        ( crossbar_width/2 - hole_offset, crossbar_depth/2),
        (-crossbar_width/2 + hole_offset, crossbar_depth/2),
    ])
    .hole(hole_dia)
)