import cadquery as cq
import math

# Create the flat plate with three blind pockets
plate = (
    cq.Workplane("XY")
      .circle(15)           # plate outer radius 15 mm
      .extrude(3)           # plate thickness 3 mm
      .faces(">Z")
      .workplane()
)
# positions for the three pockets at 120° intervals, radius 7 mm
positions = [
    (7 * math.cos(math.radians(i * 120)), 7 * math.sin(math.radians(i * 120)))
    for i in range(3)
]
plate = (
    plate
      .pushPoints(positions)
      .circle(3)            # pocket diameter 6 mm (radius 3 mm)
      .cutBlind(2)          # pocket depth 2 mm
)

# Create the matching shallow cup (lid) with inner cavity
lid = (
    cq.Workplane("XY")
      .circle(15)           # outer radius 15 mm
      .extrude(5)           # total cup height 5 mm
      .faces(">Z")
      .workplane()
      .circle(13.5)         # inner cavity radius 13.5 mm (wall thickness 1.5 mm)
      .cutBlind(4.5)        # cavity depth 4.5 mm, leaving 0.5 mm bottom
)
# translate the lid to the right so it does not intersect the plate
lid = lid.translate((40, 0, 0))

# Combine both solids into the final result
result = plate.union(lid)