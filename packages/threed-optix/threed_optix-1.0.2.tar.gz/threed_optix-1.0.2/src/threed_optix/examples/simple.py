#!/usr/bin/env python3


import threed_optix.api as opt


def main():
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    setups = api.get_setups()
    print("setups:")
    for s in setups:
        print(f"\t{s}")
    print()

    setup = setups[0]
    api.fetch(setup)
    print(f"parts in '{setup}' setup")
    for p in setup.parts:
        print(f"\t{p}")
    print()

    part = setup.parts[0]
    api.fetch(part)
    print(f"pose of '{part.label}' part:                {part.pose}")
    part.pose.position.x += 33.66
    api.update(part)
    api.fetch(part)
    print(f"pose of '{part.label}' part after updating: {part.pose}")
    print()

    result = api.run(setup)
    api.fetch(result)
    print("simulation result:")
    print(result.data)


if __name__ == '__main__':
    main()
