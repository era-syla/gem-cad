import cadquery as cq

# Parameters
r = 5       # pipe radius
H = 40      # height of the two end vertical pipes
L1 = 30     # length from left elbow tangent to tee center
L2 = 60     # spacing between left and right elbows along main run
L3 = 30     # length from tee center to right elbow tangent
stubH = 20  # height of the small tee stub

# Left vertical pipe
vleft = cq.Workplane("XY").circle(r).extrude(H)

# Main horizontal pipe
totalLength = L1 + L2 + L3
horiz = cq.Workplane("YZ").circle(r).extrude(totalLength)

# Right vertical pipe
vright = cq.Workplane("XY", origin=(totalLength, 0, 0)).circle(r).extrude(H)

# Tee stub (vertical)
stub = cq.Workplane("XY", origin=(L1 + L2/2, 0, 0)).circle(r).extrude(stubH)

# Combine all parts
result = vleft.union(horiz).union(vright).union(stub)