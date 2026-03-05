import cadquery as cq

# Parameters
d_flange = 30.0
d_mid = 20.0
d_small = 15.0
h_flange = 5.0
h_mid = 60.0
h_small = 10.0
d_hole = 8.0

# Build geometry
result = (
    cq.Workplane("XY")
      # Bottom flange
      .circle(d_flange/2).extrude(h_flange)
      # Middle cylinder
      .workplane(offset=h_flange).circle(d_mid/2).extrude(h_mid)
      # Top flange
      .workplane(offset=h_mid).circle(d_flange/2).extrude(h_flange)
      # Top small stub
      .workplane(offset=h_flange).circle(d_small/2).extrude(h_small)
      # Hole through all
      .faces(">Z").workplane().circle(d_hole/2).cutThruAll()
)