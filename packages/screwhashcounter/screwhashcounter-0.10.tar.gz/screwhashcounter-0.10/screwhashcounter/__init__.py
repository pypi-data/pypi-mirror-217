from collections import defaultdict


def countitems(arg:list|tuple, /) -> list[tuple]:
    """
    Count the occurrences of items in a list, tuple and return a list of tuples with the item and its count.

    Args:
        arg (list|tuple): The list|tuple containing items to be counted.

    Returns:
        list[tuple]: A list of tuples where each tuple contains an item and its count.

    Example:
        from screwhashcounter import countitems
        counted_items = countitems(
            ["mississippi", [1, 2], [1, 2], {34, 4, 3}, {1: 2}, {1: 2}, None, 3]
        )
        print(counted_items)
        # Output: [('mississippi', 1), ([1, 2], 2), ({34, 3, 4}, 1), ({1: 2}, 2), (None, 1), (3, 1)]
    """
    d = defaultdict(int)
    tmpdict = {}
    for k in arg:
        try:
            d[k] += 1
        except TypeError:
            strrep = f"{k}{repr(k)}"
            if strrep not in tmpdict:
                tmpdict[strrep] = k
            d[strrep] += 1
    finalresults = []
    for k, v in d.items():
        if k in tmpdict:
            finalresults.append((tmpdict[k], v))
        else:
            finalresults.append((k, v))
    return finalresults
