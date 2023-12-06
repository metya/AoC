import os

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def parse(example_data):
    ind = 0
    while ind < len(example_data):
        if example_data[ind].startswith("seeds:"):
            seeds = [int(n) for n in example_data[ind][7:].split()]
        elif example_data[ind].startswith("seed-to-soil map:"):
            ind += 1
            seed_to_soil = []
            while example_data[ind] != "":
                seed_to_soil.append([int(n) for n in example_data[ind].split()])
                ind += 1
        elif example_data[ind].startswith("soil-to-fertilizer map:"):
            ind += 1
            soil_to_fertilizer = []
            while example_data[ind] != "":
                soil_to_fertilizer.append([int(n) for n in example_data[ind].split()])
                ind += 1
        elif example_data[ind].startswith("fertilizer-to-water map:"):
            ind += 1
            fertilizer_to_water = []
            while example_data[ind] != "":
                fertilizer_to_water.append([int(n) for n in example_data[ind].split()])
                ind += 1
        elif example_data[ind].startswith("water-to-light map:"):
            ind += 1
            water_to_light = []
            while example_data[ind] != "":
                water_to_light.append([int(n) for n in example_data[ind].split()])
                ind += 1
        elif example_data[ind].startswith("light-to-temperature map:"):
            ind += 1
            light_to_temperature = []
            while example_data[ind] != "":
                light_to_temperature.append([int(n) for n in example_data[ind].split()])
                ind += 1
        elif example_data[ind].startswith("temperature-to-humidity map:"):
            ind += 1
            temperature_to_humidity = []
            while example_data[ind] != "":
                temperature_to_humidity.append(
                    [int(n) for n in example_data[ind].split()]
                )
                ind += 1
        elif example_data[ind].startswith("humidity-to-location map:"):
            ind += 1
            humidity_to_location = []
            while ind < len(example_data):
                humidity_to_location.append([int(n) for n in example_data[ind].split()])
                ind += 1
        ind += 1
    return (
        seeds,  # type: ignore
        seed_to_soil,  # type: ignore
        soil_to_fertilizer,  # type: ignore
        fertilizer_to_water,  # type: ignore
        water_to_light,  # type: ignore
        light_to_temperature,  # type: ignore
        temperature_to_humidity,  # type: ignore
        humidity_to_location,  # type: ignore
    )  # type: ignore


def get_maps(
    seeds,
    seed_to_soil,
    soil_to_fertilizer,
    fertilizer_to_water,
    water_to_light,
    light_to_temperature,
    temperature_to_humidity,
    humidity_to_location,
):
    mapping = {
        0: seed_to_soil,
        1: soil_to_fertilizer,
        2: fertilizer_to_water,
        3: water_to_light,
        4: light_to_temperature,
        5: temperature_to_humidity,
        6: humidity_to_location,
    }
    location = None
    for seed in seeds:
        temp = seed
        for m in mapping.values():
            for d, s, r in m:
                if temp <= s + r - 1 and temp >= s:
                    temp = temp + d - s
                    break
        location = min(temp, location) if location else temp
    print(location)
    return location


def get_ranges(
    seeds,
    seed_to_soil,
    soil_to_fertilizer,
    fertilizer_to_water,
    water_to_light,
    light_to_temperature,
    temperature_to_humidity,
    humidity_to_location,
):
    mapping = {
        0: seed_to_soil,
        1: soil_to_fertilizer,
        2: fertilizer_to_water,
        3: water_to_light,
        4: light_to_temperature,
        5: temperature_to_humidity,
        6: humidity_to_location,
    }
    location = None
    for seed, ran in list(zip(seeds[0::2], seeds[1::2])):
        seed_intervals = [(seed, seed + ran - 1)]
        for m in mapping.values():
            temp = []
            for start, end in seed_intervals:
                for d, s, r in m:
                    if s <= start and end < s + r:
                        temp.append((start - s + d, end - s + d))
                        break
                    elif s > start and s <= end and end < s + r:
                        seed_intervals.append((start, s - 1))
                        temp.append((d, d + end - s))
                        break
                    elif start < s + r and end >= s + r and start >= s:
                        seed_intervals.append((s + r, end))
                        temp.append((d + start - s, d + r - 1))
                        break
                    elif start < s and end >= s + r:
                        seed_intervals.append((start, s - 1))
                        temp.append((d, d + r - 1))
                        seed_intervals.append((s + r, end))
                        break
                else:
                    temp.append((start, end))
            seed_intervals = temp
        location = (
            min(min(seed_intervals)[0], location)
            if location
            else min(seed_intervals)[0]
        )
    print(location)
    return location


get_maps(*parse(example_data))
get_maps(*parse(input_data))
get_ranges(*parse(example_data))
get_ranges(*parse(input_data))
