import cadquery as cq

# Define the rear dropout shape
dropout = cq.Workplane("XY").circle(10).extrude(5)

# Define the chainstay shape
chainstay_profile = cq.Workplane("XZ").moveTo(5, 0).lineTo(0, 50).lineTo(-5, 0).close()
chainstay = chainstay_profile.extrude(15)

# Define the seatstay shape
seatstay_profile = cq.Workplane("XZ").moveTo(2, 0).lineTo(0, 45).lineTo(-2, 0).close()
seatstay = seatstay_profile.extrude(10)

# Position and combine the components
result = (
    cq.Workplane("XY")
    .add(dropout)
    .moveTo(55, 0).add(chainstay)
    .moveTo(60, 50).add(chainstay)
    .moveTo(60, 55).add(seatstay)
    .moveTo(55, 5).add(seatstay)
)

# Create connections and combine
result = result.union(result.mirror("YZ"))