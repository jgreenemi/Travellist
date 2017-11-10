import logging

# Modules elsewhere in the package can't be imported unless we modify the PYTHONPATH env var to make them findable.
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from travellist.data_ingestion.db_interactor import DBInteractor
from travellist.toolkit.file_toolkit import file_interpreter

# The data_populator module is used for populating the database with location data.
# Also includes mock data loading for dev purposes.


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
        '''
        We're in a dev environment so load a known-good JSON file of data.
        :return: dict
        '''
        try:
            mock_data = file_interpreter('travellist/resources/mock_data/mock_location_data.json')
            items_loaded = mock_data.keys().__len__
            logging.debug('mock_load: Loaded {} items!'.format(items_loaded))
            return mock_data
        except Exception as e:
            return {'failure': e}

if __name__ == '__main__':
    '''
    Test the mock_load method.
    '''
    from pprint import pprint

    populator = DataPopulator(mock=True)
    mock_data = populator.mock_load()
    print('Found {} keys from the mock data!'.format(mock_data.keys().__len__()))
    for k, v in mock_data.items():
        print('Country {} has {} attributes and {} provinces.'.format(
            k,
            v.keys().__len__(),
            v['provinces'].__len__()
        ))

    # Try writing the mock data to the dev table.
    dbi = DBInteractor(mock=True)
    write_response = dbi.write(data_to_write=mock_data)
    pprint(write_response)
