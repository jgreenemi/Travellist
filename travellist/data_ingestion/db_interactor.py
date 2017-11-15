import boto3
import logging

class DBInteractor:
    def __init__(self, mock=False):
        self.mock = mock
        self.tablename = 'travellist'
        if self.mock:
            self.tablename = '{}-development'.format(self.tablename)
        self.dbclient = boto3.client('dynamodb')
        return

    def drop(self):
        return self.dbclient.delete_table(TableName=self.tablename)

    def describe(self):
        return self.dbclient.describe_table(TableName=self.tablename)

    def read(self):
        return self.dbclient.get_item(
            TableName=self.tablename,
            Key={
                'country': {
                    'S': 'US'
                }
            }
        )

    def write(self, data_to_write):
        '''
        Given a dict, write put items into the table. Map dict items to keys in the table at this point.
        :param data_to_write: dict
        :return: dict
        '''

        write_result = {}

        try:
            # Do a simple write of whatever data came in. Assume that we only have a country ID to write at this point.
            write_result['response'] = []
            for k, v in data_to_write.items():

                # Format the data_to_write table for DynamoDB insertion.
                # This is very much not preferable as it makes assumptions about the incoming data, which is not
                # scalable. As a basic proof of concept for loading data into the table I'm flattening everything down
                # to strings before writing them, just to get something written.
                formatted_dict = {
                    'country': {
                        'S': k
                    }
                }

                for subkey, subvalue in v.items():
                    formatted_dict[subkey] = {
                        'S': str(subvalue)
                    }

                from pprint import pprint
                pprint(formatted_dict)

                logging.warning('Writing new attributes for {} into table!'.format(k))
                put_response = self.dbclient.put_item(
                    TableName=self.tablename,
                    Item=formatted_dict
                )
                write_result['response'].append(put_response)

            write_result['success'] = True
        except Exception as e:
            write_result = {'failure': e}

        return write_result

    def instantiate(self):
        '''
        Create a DynamoDB table. Doesn't check if it already exists, just tries to create it.
        Leveraging documentation example here:
        http://boto3.readthedocs.io/en/latest/guide/dynamodb.html
        :return: dict
        '''
        db_instantiation_result = {}

        try:
            # We'll try to create a table here. Check what environment we're running in when setting the name.
            table = self.dbclient.create_table(
                TableName=self.tablename,
                KeySchema=[
                    {
                        'AttributeName': 'country',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'country',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait for a table matching 'tablename' to be created.
            logging.warning('Waiting for DynamoDB table to be created...')
            table.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)

            # Once created, demonstrate it by printing contents.
            db_instantiation_result['itemcount'] = table.item_count

            db_instantiation_result['success'] = True
        except Exception as e:
            db_instantiation_result = {'failure': e}

        return db_instantiation_result

    def list_all(self, index='US'):
        '''
        Get all items from a DynamoDB table. This can be a very expensive call if the table has many records, so only
        use in dev.
        :return: dict
        '''

        db_full_result = {}

        try:
            table = self.dbclient.scan(
                TableName=self.tablename,
                Limit=10
            )

            db_full_result['table'] = table
            db_full_result['success'] = True
        except Exception as e:
            db_full_result = {'failure': e}
        return db_full_result

if __name__ == '__main__':
    from pprint import pprint
    logging.info('Instantiating a mock DynamoDB table.')
    dbi = DBInteractor(mock=True)

    #print('\n---- Creating test table.')
    #dbi_result = dbi.instantiate()
    #pprint(dbi_result)

    #print('\n---- Describing test table.')
    #dbi_result = dbi.describe()
    #pprint(dbi_result)

    #print('\n---- Getting an item from the test table.')
    #dbi_result = dbi.read()
    #pprint(dbi_result)

    print('\n---- Getting all items from test table.')
    dbi_result = dbi.list_all()
    pprint(dbi_result)

    #print('\n---- Dropping test table.')
    #dbi_result = dbi.drop()
