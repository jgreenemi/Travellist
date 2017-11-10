def file_interpreter(name):
    '''
    Take an absolute file path as input, return a dict response. In the case of failure, the returned dict will have a
    single key of the name 'failure' with a value of the exception.
    :param name: Absolute file path, as string.
    :return: Dictionary of either file contents, or {'failure': '<Exception message>'}
    :rtype: dict
    '''
    import json

    try:
        with open(name) as f:
            json_contents = json.load(f)
            f.close()
            return json_contents
    except Exception as e:
        return {'failure': e}

if __name__ == '__main__':
    '''
    Test that the fileloader works by reading a file from disk. Assumed to be run from the package root.
    '''
    from pprint import pprint

    print('Testing file_toolkit.py.')
    result = file_interpreter('resources/mock_data/mock_location_data.json')
    # print(type(result))
    # pprint(result)

    if 'failure' not in result.keys():
        print('Loading succeeded! {} keys found in file.'.format(result.__len__()))
    else:
        print('Loading failed! {}'.format(result))
