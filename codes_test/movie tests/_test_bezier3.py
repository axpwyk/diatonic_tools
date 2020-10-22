from movie import *

position_1 = (0, 0)
position_2 = (1, 1)
control_point_1 = (0.2, 0.8)
control_point_2 = (0.75, 1)

out = bezier3t(np.linspace(0, 1, 100), position_1, position_2, control_point_1, control_point_2, 1e-10)
print(out)

plt.plot(out[:, 0], out[:, 1], marker='x')
plt.arrow(position_1[0], position_1[1], control_point_1[0]-position_1[0], control_point_1[1]-position_1[1])
plt.arrow(position_2[0], position_2[1], control_point_2[0]-position_2[0], control_point_2[1]-position_2[1])
plt.xlabel('time')
plt.ylabel('position (x or y or z)')
plt.show()
