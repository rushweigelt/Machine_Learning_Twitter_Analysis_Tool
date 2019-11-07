from pprint import pformat


class DataError(Exception):
    pass


def validated(retrieve_func):
    def retrieve(*args, data_format=None, **kwargs):
        dataset = retrieve_func(*args, **kwargs)
        if not dataset:
            raise DataError(f'Dataset is empty.')
        elif format:
            for data in dataset:
                if get_format(data) != data_format:
                    s = pformat(data_format)
                    raise DataError(f'Retrieved dataset does not have the expected format:\n{s}')
        return dataset
    return retrieve


def get_format(data):
    t = type(data)
    if t is dict:
        return {(key, get_format(element)) for (key, element) in data.items()}
    elif t in {tuple, list, set}:
        return t(get_format(element) for element in data)
    else:
        return t
