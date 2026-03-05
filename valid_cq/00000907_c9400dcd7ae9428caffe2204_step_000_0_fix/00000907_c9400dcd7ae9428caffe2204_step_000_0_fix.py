import cadquery as cq

# Thickness of sheet metal
t = 2.0

# === Main front panel ===
panel_w = 120
panel_h = 90

# Create main rectangular panel
front_panel = (
    cq.Workplane("XY")
    .rect(panel_w, panel_h)
    .extrude(t)
)

# Cut large central rectangular opening
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .rect(80, 50)
    .cutThruAll()
)

# Cut slot on right side
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(55, 0)
    .rect(6, 30)
    .cutThruAll()
)

# Cut slot on left side
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(-55, 0)
    .rect(6, 30)
    .cutThruAll()
)

# Cut notch bottom center
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(0, -40)
    .rect(30, 8)
    .cutThruAll()
)

# Cut notch top center
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(0, 40)
    .rect(30, 8)
    .cutThruAll()
)

# Cut small rectangular cutout bottom left of center opening
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(-20, -20)
    .rect(15, 8)
    .cutThruAll()
)

# Cut small rectangular cutout bottom right of center opening
front_panel = (
    front_panel
    .faces(">Z")
    .workplane()
    .center(20, -20)
    .rect(15, 8)
    .cutThruAll()
)

# === Second identical panel (offset behind) ===
second_panel = (
    cq.Workplane("XY")
    .rect(panel_w, panel_h)
    .extrude(t)
    .translate((0, 0, -20))
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .rect(80, 50)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(55, 0)
    .rect(6, 30)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(-55, 0)
    .rect(6, 30)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(0, -40)
    .rect(30, 8)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(0, 40)
    .rect(30, 8)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(-20, -20)
    .rect(15, 8)
    .cutThruAll()
)

second_panel = (
    second_panel
    .faces(">Z")
    .workplane()
    .center(20, -20)
    .rect(15, 8)
    .cutThruAll()
)

# === Top rail / bracket ===
top_rail = (
    cq.Workplane("XY")
    .rect(panel_w + 20, 12)
    .extrude(t)
    .translate((0, 55, 30))
)

# Small hole in top rail
top_rail = (
    top_rail
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(3)
    .cutThruAll()
)

# === Side flange on top rail ===
side_flange = (
    cq.Workplane("XZ")
    .workplane(offset=6)
    .rect(panel_w + 20, 15)
    .extrude(t)
    .translate((0, 55, 22))
)

# Combine all parts
result = (
    front_panel
    .union(second_panel)
    .union(top_rail)
    .union(side_flange)
)