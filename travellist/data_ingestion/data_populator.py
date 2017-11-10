import logging
from travellist.toolkit.file_toolkit import file_interpreter

# Module for populating the database with location data. Also includes mock data loading for dev purposes.

class DataPopulator:
    def __init__(self, mock=False):
        self.mock = mock
        return

    def database_writer(self, data_to_write):
        '''
        Generic writer for taking a dict and inserting it directly to the database. Data is assumed to be cleaned before
        it gets to this point, but may prefer to do validation at this stage rather than assume it's good.
        :param data_to_write: dict
        :return: dict
        '''
        writer_result = {}

        try:
            if self.mock:
                data_to_write = self.mock_load()

            writer_result = {'success': True}
        except Exception as e:
            writer_result = {'failure': e}

        return writer_result

    def mock_load(self):
        try:
            mock_data = file_interpreter('resources/mock_data/mock_location_data.json')
            items_loaded = mock_data.keys().__len__
            logging.debug('mock_load: Loaded {} items!'.format(items_loaded))
            return mock_data
        except Exception as e:
            return {'failure': e}

if __name__ == '__main__':
    from pprint import pprint
    populator = DataPopulator(mock=True)
    pprint(populator.mock_load())

