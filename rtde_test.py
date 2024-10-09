import rtde_control
import rtde_receive
import time

from splay_tree import *

rtde_c = rtde_control.RTDEControlInterface("169.254.9.43")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.9.43")

# create initial splay tree
root = Node(Vector(0, 0, 1), "up", math.pi/4)
root.insert(Node(Vector(0, 0, -1), "down", math.pi/4))
root.insert(Node(Vector(-1, 0, 0), "left", math.pi/4))
root.insert(Node(Vector(1, 0, 0), "right", math.pi/4))
root.insert(Node(Vector(0, -1, 0), "forward", math.pi/4))
root.insert(Node(Vector(0, 1, 0), "backward", math.pi/4))

velocity = 0.5
acceleration = 0.3
blend = 0.1

tcp = rtde_r.getActualTCPPose()
print(tcp)
path = []
tcp[2] += 0.3
path.append(tcp + [velocity, acceleration, blend])
path.append(rtde_r.getActualTCPPose() + [velocity, acceleration, blend])

rtde_c.moveL(path, True)

while True:
    vel = rtde_r.getTargetTCPSpeed()
    print(vel)
    print(root.access(Vector(*vel[:3])))
    print()
    time.sleep(0.1)