#!/usr/bin/env python3


import threed_optix.api as opt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

setups = api.get_setups()
setup = [s for s in setups if s.name == 'setup_a'][0]
print(f"working with '{setup}' setup")
api.fetch(setup)

part = setup.parts[1]
print(f"moving '{part}' part")
api.fetch(part)

original_z = part.pose.position.z


def run_simulation():
    result = api.run(setup)
    api.fetch(result)
    data = result.data
    data = data[data['hit_surface_idx'] == 3]
    return data


data = run_simulation()
min_x = (data['Hx'].min(), data['Hx'].max())
min_y = (data['Hy'].min(), data['Hy'].max())

fig, ax = plt.subplots(figsize=(10, 10))
frames = 60

areas = []
z_positions = []


def animate(i):
    ax.clear()
    print(f"running simulation for lens position {part.pose.position}")
    data = run_simulation()

    ax.scatter(data['Hx'], data['Hy'])
    ax.set_title(f'z position = {part.pose.position.z}')
    ax.set_xlabel('Hx')
    ax.set_ylabel('Hy')
    ax.set_xlim(min_x[0], min_x[1])
    ax.set_ylim(min_y[0], min_y[1])

    z_positions.append(part.pose.position.z)
    area = (data['Hx'].max() - data['Hx'].min()) * (data['Hy'].max() - data['Hy'].min())
    areas.append(area)

    part.pose.position.z += 1
    api.update(part)


ani = animation.FuncAnimation(fig, animate, frames=frames)
ani.save('scatter.gif', writer='pillow')

plt.close()

min_area = areas.index(min(areas))
print(f'z position of minimum area: {z_positions[min_area]}')

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(z_positions, areas, markevery=[min_area], marker='o', ms=20, mec='r', mfc='None')
ax.set_xlabel('z position')
ax.set_ylabel('area')
plt.show()

part.pose.position.z = original_z
api.update(part)

