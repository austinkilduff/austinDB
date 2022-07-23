# austinDB: a very special database library for very special people
import json

class Database:
    # Given a JSON filename, initialize the database
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.db = {}

        try:
            self.load_database()
        except:
            self.save_database()

        self.tables = [Table(self, table_name) for table_name in self.db]

    ''' File operations '''
    def load_database(self):
        with open(self.db_filename) as db_f:
            self.db = json.loads(db_f.read())

    def save_database(self):
        with open(self.db_filename, "w") as db_f:
            db_f.write(json.dumps(self.db))

    ''' Table operations '''
    # Given a table name and list of field names, add a table
    def create(self, table_name, fields):
        self.db[table_name] = [fields]
        self.tables.append(Table(self, table_name))
        self.save_database()

    # Given a table name, return the contents of the table
    def read(self, table_name):
        for table in self.tables:
            if table_name == table.table_name:
                return table

    # Given a table name, remove the table
    def delete(self, table_name):
        self.db.pop(table_name, None)
        for i, table in enumerate(self.tables):
            if table_name == table.table_name:
                self.tables.pop(i)
        self.save_database()

# Table class
class Table:
    # Given a Database object and a table name, create the table
    def __init__(self, database, table_name):
        self.database = database
        self.table_name = table_name

    ''' CRUD operations '''
    # Given a list of values, create a row in the table
    def create(self, values):
        self.database.db[self.table_name].append(values)
        self.database.save_database()

    # Given a list of fields to read, list of fields to test, and list of test functions, read the fields from matching rows in the table
    def read(self, read_field_names=[], test_field_names=[], test_functions=[(lambda *x: True)]):
        matching_rows = []

        db_field_names = self.database.db[self.table_name][0]
        if len(read_field_names) == 0:
            read_field_names = db_field_names
        db_read_field_indices = [db_field_names.index(read_field_name) for read_field_name in read_field_names]
        db_test_field_indices = [db_field_names.index(test_field_name) for test_field_name in test_field_names]

        for db_row in self.database.db[self.table_name][1:]:
            test_function_evaluations = []

            for test_function_index, db_test_field_index in enumerate(db_test_field_indices):
                test_function = test_functions[test_function_index]
                db_test_value = db_row[db_test_field_index]
                test_function_evaluations.append(test_function(db_test_value))

            if False not in test_function_evaluations:
                matching_rows.append([db_row[db_read_field_index] for db_read_field_index in db_read_field_indices])

        return matching_rows

    # Given a list of fields to update, list of updated values, list of fields to test, and list of test functions, update the fields from matching rows in the table
    def update(self, update_field_names, update_values, test_field_names=[], test_functions=[(lambda *x: True)]):
        db_field_names = self.database.db[self.table_name][0]
        db_update_field_indices = [db_field_names.index(update_field_name) for update_field_name in update_field_names]
        db_test_field_indices = [db_field_names.index(test_field_name) for test_field_name in test_field_names]

        for db_row in self.database.db[self.table_name][1:]:
            test_function_evaluations = []

            for test_function_index, db_test_field_index in enumerate(db_test_field_indices):
                test_function = test_functions[test_function_index]
                db_test_value = db_row[db_test_field_index]
                test_function_evaluations.append(test_function(db_test_value))

            if False not in test_function_evaluations:
                for update_value_index, db_update_field_index in enumerate(db_update_field_indices):
                    db_row[db_update_field_index] = update_values[update_value_index]

        self.database.save_database()

    # Given a list of fields to test and list of test functions, delete the matching rows from the table
    def delete(self, test_field_names, test_functions):
        db_field_names = self.database.db[self.table_name][0]
        db_test_field_indices = [db_field_names.index(test_field_name) for test_field_name in test_field_names]

        for db_row in self.database.db[self.table_name][1:]:
            test_function_evaluations = []

            for test_function_index, db_test_field_index in enumerate(db_test_field_indices):
                test_function = test_functions[test_function_index]
                db_row_value = db_row[db_test_field_index]
                test_function_evaluations.append(test_function(db_row_value))

            if False not in test_function_evaluations:
                self.database.db[self.table_name].remove(db_row)

        self.database.save_database()
