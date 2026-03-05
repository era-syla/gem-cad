import cadquery as cq

# Parameters
rod_length = 200
rod_diameter = 8
rod_spacing = 40
bracket_height_position = rod_length * 0.25
bracket_width = 20
bracket_depth = 10
bracket_thickness = 8
bracket_fillet = 1

# Create two parallel rods
rod1 = cq.Workplane("XY").circle(rod_diameter/2).extrude(rod_length)
rod2 = cq.Workplane("XY").center(rod_spacing, 0).circle(rod_diameter/2).extrude(rod_length)

# Combine rods
result = rod1.union(rod2)

# Create a bracket that attaches to both rods
bracket = (
    cq.Workplane("XY", origin=(rod_spacing/2, 0, bracket_height_position))
      .rect(bracket_width, bracket_depth)
      .extrude(bracket_thickness)
      .faces(">Z")
      .edges()
      .fillet(bracket_fillet)
)

# Combine bracket with rods
result = result.union(bracket)