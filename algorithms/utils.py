from itertools import zip_longest


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    return zip_longest(*[iter(lst)] * n, fillvalue=0)
