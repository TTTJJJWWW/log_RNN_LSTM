from __future__ import division
 
def jaro(a, b):
	a_len = len(a)
	b_len = len(b)
	if a_len == 0 and b_len == 0:
		return 1
	# set the match window
	match_distance = (max(a_len, b_len) // 2) - 1
	# find the match
	a_matches = [False] * a_len
	b_matches = [False] * b_len
	matches = 0
	transpositions = 0
	for i in range(a_len):
		start = max(0, i - match_distance)
		end = min(i + match_distance + 1, b_len)
		for j in range(start, end):
			if b_matches[j]:
				continue
			if a[i] != b[j]:
				continue
			a_matches[i] = True
			b_matches[j] = True
			matches += 1
			break
	if matches == 0:
		return 0
	# find transpositions in the match
	k = 0
	for i in range(a_len):
		if not a_matches[i]:
			continue
		while not b_matches[k]:
			k += 1
		if a[i] != b[k]:
			transpositions += 1
		k += 1
	# return the jaro distance
	return ((matches / a_len) +
			(matches / b_len) +
			((matches - transpositions / 2) / matches)) / 3

if __name__ == '__main__':
	for x, y in [('this is me', 'this is em'),
				('this is me', 'this is mes'),
				('this is me', 'that is him'),
				('this is me', 'this is me')]:
		print("jaro-distance(%r, %r) = %.2f" % (x, y, jaro(x, y)))
