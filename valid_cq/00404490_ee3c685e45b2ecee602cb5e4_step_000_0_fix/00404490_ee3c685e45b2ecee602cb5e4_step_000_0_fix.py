import cadquery as cq

# Parameters
length = 45.0    # overall length in X
width = 10.0     # overall width in Y
thickness = 5.0  # overall thickness in Z
fillet_radius = 2.0
hole_diameter = 6.0
hole_offset = 15.0  # distance from center to each hole along X

# Build the main body: a rectangular bar with rounded ends
result = (
    cq.Workplane("XY")
      .rect(length, width)         # base rectangle
      .extrude(thickness)          # extrude to thickness
      .edges("|Z")                 # select all edges running in Z direction
      .fillet(fillet_radius)       # fillet them
      # Drill two holes through the top face
      .faces(">Z")
      .workplane()
      .center(-hole_offset, 0)     
      .hole(hole_diameter)
      .center(2 * hole_offset, 0)
      .hole(hole_diameter)
)

# result now holds the final solid geometry.