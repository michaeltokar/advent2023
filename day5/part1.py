import sys
import re

# For a given source, represents the destination mapping, and the length of the range of the mapping
class MapRange:
	def __init__(self, dest, rlength):
		self.dest = dest
		self.rlength = rlength

	def __eq__(self, other):
		if isinstance(other, MapRange):
			return (self.dest, self.rlength) == (other.dest, other.rlength)
		return False

	def __hash__(self):
		# Ensure instances of MapRange are hashable
		return hash((self.dest, self.rlength))

	def __str__(self):
		return f"{self.dest} > {self.rlength})"



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
	mapping[src] = MapRange(dest, rlength)


# Look up src in mapping. If not present return the src.
def get_or_src(mapping, src):
	# Find the closest src key to what we're looking for
	sorted_keys = sorted(mapping.keys())
	closest_key = None
	for k in sorted_keys:
		if k <= src:
			closest_key = k

	if closest_key is None:
		return src

	# Get the MapRange object associated to the closest key
	# Check that src falls between closest_key and rlength
	mr = mapping.get(closest_key)
	delta = src - closest_key
	if delta < mr.rlength:
		return mr.dest + delta

	# Otherwise it was not mapped, so return src
	return src


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
