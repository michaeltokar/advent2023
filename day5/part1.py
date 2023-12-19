import sys
import re

seeds = set()

seed_soil = {}
soil_fert = {}
fert_watr = {}
watr_ligt = {}
ligt_temp = {}
temp_humi = {}
humi_loca = {}
results = {}

# Map definitions
maps = {}
maps['seed-to-soil'] = seed_soil
maps['soil-to-fertilizer'] = soil_fert
maps['fertilizer-to-water'] = fert_watr
maps['water-to-light'] = watr_ligt
maps['light-to-temperature'] = ligt_temp
maps['temperature-to-humidity'] = temp_humi
maps['humidity-to-location'] = humi_loca

# Convert an array of strings to an array of numbers
def to_number_set(arr):
    return set([ int(x) for x in arr ])


# Add mapping formula to destination array
def append_map(mapping, line):
	# Format of line: destination, source, range length
	parts = line.split(" ")
	dest, src, rlength = [ int(x) for x in parts ]
	for i in range(0, rlength):
		mapping[src + i] = dest + i
	#print(f"{line} added to map")
	#print(f"New map: {mapping}")


# Look up src in mapping. If not present return the src.
def get_or_src(mapping, src):
	dest = mapping.get(src)
	if dest is None:
		return src
	return dest


# Plant a seed and see where it goes
def plant_seed(seed):
	soil = get_or_src(seed_soil, seed)
	fert = get_or_src(soil_fert, soil)
	watr = get_or_src(fert_watr, fert)
	ligt = get_or_src(watr_ligt, watr)
	temp = get_or_src(ligt_temp, ligt)
	humi = get_or_src(temp_humi, temp)
	loca = get_or_src(humi_loca, humi)
	return loca


# Read input lines until EOF (Ctrl+D)
mode = None
for line in sys.stdin:
	if re.match(r'^seeds: ', line):
		seeds = to_number_set(line.strip()[7:].split(" "))
		continue
	elif re.match(r'^\d+', line):
		append_map(maps[mode], line.strip())
		continue


	mapstr = re.search(r'(.*) map:', line)
	if mapstr:
		mapname = mapstr.group(1)
		mode = mapname

lowest_result = None
for s in seeds:
	results[s] = plant_seed(s)
	if lowest_result is None or lowest_result > results[s]:
		lowest_result = results[s]

print(results)
print(f"Lowest result is: {lowest_result}")
