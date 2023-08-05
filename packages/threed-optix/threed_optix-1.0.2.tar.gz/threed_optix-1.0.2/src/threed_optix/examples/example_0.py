#!/usr/bin/env python3


import threed_optix.api as opt
import matplotlib.pyplot as plt


def main():
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    setups = api.get_setups()
    setup = [s for s in setups if s.name == 'setup_a'][0]
    print(f"working with '{setup}' setup")
    api.fetch(setup)

    part = setup.parts[1]
    print(f"moving '{part}' part")
    api.fetch(part)

    original_z = part.pose.position.z

    n = 3
    for i in range(n):
        print(f"running simulation for lens position {part.pose.position}")
        result = api.run(setup)
        api.fetch(result)

        file_name = f'example_0_result_{i}.csv'
        result.data.to_csv(file_name)

        data = result.data
        data = data[data['hit_surface_idx'] == 3]
        data.plot.scatter(x='Hx', y='Hy', figsize=(10, 10))
        plt.show()

        part.pose.position.z += 1
        api.update(part)

    part.pose.position.z = original_z
    api.update(part)


if __name__ == '__main__':
    main()
