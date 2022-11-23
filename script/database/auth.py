from config import postgre_config
import connector
import psycopg2

class AuthenticationError(Exception):
    pass

def login(username, password, columns=('employee_id', 'username', 'password', 'name', 'phone_number', 'address', 'department')):
    '''
        Return an attribute dictionary of employee with the username and password.
    '''
    sql_statement = f'SELECT {", ".join(columns)} FROM employee WHERE username=%s AND password=%s'

    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (username, password))

    column_values = cursor.fetchone()

    # Raise an exception if no such username and password combination exists
    if column_values is None:
        raise AuthenticationError("username or password is incorrect!")

    employee_information= {column:value for column, value in zip(columns,column_values)}

    cursor.close()
    connection.close()

    return employee_information