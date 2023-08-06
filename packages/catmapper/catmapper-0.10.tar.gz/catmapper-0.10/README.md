# Maps the elements of an iterable to categories using bisect

## pip install catmapper

#### Tested against Windows 10 / Python 3.10 / Anaconda 

	
```python
Args:
	iterable (iterable): The iterable containing the elements to be categorized.
	cats (list[list, list] | list[tuple | list]): The categories used for mapping. It can be provided in two formats:
		- A list of two lists, where the first list represents the category labels and the second list represents
		  the corresponding values. The values don't have to be in ascending order.
		- A list of pairs, where each pair consists of a category label and its corresponding value.

Returns:
	list[tuple]: A list of tuples, where each tuple contains an element from the 'iterable' and its corresponding category.

Raises:
	TypeError: If the 'cats' argument is not in the expected format or if the values are not in ascending order.

Examples:
	import sys
	from catmapper import category_mapping
	# Example 1: Using a list with 2 lists
	cats_ = [['barato', 'mais ou menos', 'caro', 'muito caro', 'absurdo'],
			 [1.3, 2, 3.1, 6.5, sys.maxsize]]
	cervejas = [
		("original", 2.5),
		("Skol", 0.5),
		("becks", 16),
		("brahma", 1.4),
		("heineken", 5.5),
	]
	print(category_mapping(cervejas, cats_))
	# Output:
	# [(('original', 2.5), 'caro'), (('Skol', 0.5), 'barato'), (('becks', 16), 'absurdo'),
	# (('brahma', 1.4), 'mais ou menos'), (('heineken', 5.5), 'muito caro')]

	# Example 2: Using a list of pairs
	cats_ = [
		("barato", 1.3),
		("mais ou menos", 2),
		("caro", 3.1),
		("muito caro", 6.5),
		("absurdo", sys.maxsize),
	]
	# also ok:
	cats_ = [
		("muito caro", 6.5),
		("mais ou menos", 2),
		("caro", 3.1),
		("absurdo", sys.maxsize),
		("barato", 1.3),
	]
	print(category_mapping(cervejas, cats_))
	# Output:
	# [(('original', 2.5), 'caro'), (('Skol', 0.5), 'barato'), (('becks', 16), 'absurdo'),
	# (('brahma', 1.4), 'mais ou menos'), (('heineken', 5.5), 'muito caro')]
```