import cadquery as cq

# Define dimensions
leg_length = 100.0
leg_thickness = 5.0
leg_height = 10.0
support_height = 50.0

# Create the two legs
legs = (cq.Workplane("XY")
        .box(leg_length, leg_thickness, leg_height)
        .faces(">Y")
        .box(leg_length, leg_thickness, leg_height)
        )

# Create the triangular support
triangle = (cq.Workplane("XY")
            .moveTo(0, leg_thickness / 2)
            .lineTo(leg_length, leg_thickness / 2)
            .lineTo(0, support_height)
            .close()
            .extrude(leg_thickness)
            )

# Combine the legs and the support
result = legs.union(triangle)