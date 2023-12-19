import sys
import re

# For a given source, represents the destination mapping, and the length of the range of the mapping
class MapRange:
	def __init__(self, src, dest, rlength):
		self.src = src
		self.dest = dest
		self.rlength = rlength

	def __eq__(self, other):
		if isinstance(other, MapRange):
			return (self.src, self.dest, self.rlength) == (other.src, other.dest, other.rlength)
		return False

	def __hash__(self):
		# Ensure instances of MapRange are hashable
		return hash((self.src, self.dest, self.rlength))

	def __str__(self):
		return f"{self.src} > {self.dest} > {self.rlength})"



seeds = {}
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
def to_numbers(arr):
	return [ int(x) for x in arr ]


# Seeds are now specified in ranges. These are similar to our MapRanges.
def to_seed_set(seeds, seed_ranges):
	# Array specifies pairs of numbers: start, range length
	for i in range(0, len(seed_ranges), 2):
		start, rlength = seed_ranges[i:i+2]
		# Seed ranges don't have a source & destination, so we reuse src
		seeds[start] = MapRange(start, start, rlength)
	


# Add mapping formula to destination array
def append_map(mapping, line):
	# Format of line: source, destination, range length
	# SWAPPED WITH PART 1
	parts = line.split(" ")
	src, dest, rlength = [ int(x) for x in parts ]
	mapping[src] = MapRange(src, dest, rlength)

# Look up src in mapping. If not present return the src.
def get_or_src(mapping, src):
	return get_or_default(mapping, src, src)

# Look up src in mapping. If not present return the default.
def get_or_default(mapping, src, default):
	# Find the closest src key to what we're looking for
	sorted_keys = sorted(mapping.keys())
	closest_key = None
	for k in sorted_keys:
		if k <= src:
			closest_key = k

	if closest_key is None:
		return default

	# Get the MapRange object associated to the closest key
	# Check that src falls between closest_key and rlength
	mr = mapping.get(closest_key)
	delta = src - closest_key
	if delta < mr.rlength:
		return mr.dest + delta

	# Otherwise it was not mapped, so return src
	return default


# Follow a location backwards to find a seed
def reverse_lookup(loca):
	humi = get_or_src(humi_loca, loca)
	temp = get_or_src(temp_humi, humi)
	ligt = get_or_src(ligt_temp, temp)
	watr = get_or_src(watr_ligt, ligt)
	fert = get_or_src(fert_watr, watr)
	soil = get_or_src(soil_fert, fert)
	seed = get_or_src(seed_soil, soil)

	# check whether this seed is valid
	result = get_or_default(seeds, seed, None)
	return result

# Read input lines until EOF (Ctrl+D)
mode = None
for line in sys.stdin:
	line = line.strip()
	if re.match(r'^seeds: ', line):
		to_seed_set(seeds, to_numbers(line[7:].split(" ")))
		continue
	elif re.match(r'^\d+', line):
		append_map(maps[mode], line)
		continue


	mapstr = re.search(r'(.*) map:', line)
	if mapstr:
		mapname = mapstr.group(1)
		mode = mapname

result = None
for loca in range(0, 999999999):
	s = reverse_lookup(loca)
	if s != None:
		result = f"Seed {s} found from location {loca}"
		break

if result is None:
	result = f"Could not find any listed seed"

print(result)
