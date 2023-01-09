import os
import sys

from getpass import getpass

import psycopg2.errors

from database.table import Employee, Product, Transaction, Transaction_Detail, PrivilegeError, Management, Finance, Storage, Can_Do_Transaction, Can_Edit_Catalog, Can_Edit_Product_Info
import database.connector as connector
import database.auth as auth

def main():
    try:
        menu = Menu()
        os.system('cls')
        while True:
            print()
            try:
                menu.select()
            except AbortOperation as e:
                print(e)
    except KeyboardInterrupt:
        print("You have exited the console app")
        sys.exit()

class AbortOperation(Exception):
    pass

class Menu:
    '''
        Menu for console app.
    '''

    def __init__(self):
        '''
            Logs user in.
        '''
        user = None
        department_class = {
            'Management':Management,
            'Finance':Finance,
            'Storage':Storage
        }

        # Logging in
        while not user:
            username = input("Username: ")
            password = getpass()
            try:
                user = Employee.login(username, password)
            except auth.AuthenticationError as exc:
                os.system('cls')
                print(str(exc))

        # Sublass casting
        try:
            type_cast = department_class[user.get_department()]
            user = type_cast(**user)
        except KeyError:
            pass

        self.user = user
        self.selections = None

    def add_product(self):
        '''
            Procedure for adding a product.
        '''
        # Asking for input
        name = input('Product name: ')
        name = None if name == '' else name
        category = input('Product category: ')
        category = None if category == '' else category
        description = input('Product description: ')
        description = None if description == '' else description
        try:
            price = int(input('Product price: '))
            if price < 0:
                raise AbortOperation("The product price can't be negative")
        except ValueError:
            raise AbortOperation('The specified product price is invalid')

        # Adding new product
        try:
            new_product = self.user.add_product(name=name, category=category, description=description, price=price)
        except PrivilegeError:
            print("You don't have the privilege to edit the catalog")
        except psycopg2.errors.NotNullViolation as exc:
            raise AbortOperation(str(exc)) from exc

        print(f"{new_product.name} has been added with the id of {new_product.product_id}")

    def show_catalog(self):
        '''
            Print out list of products
        '''
        try:
            self.user.show_catalog()
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc

    def show_product_by_id(self):
        '''
            Procedure for showing product information by its id.
        '''

        # Asking for input
        product_id = None
        while product_id is None:
            try:
                product_id = int(input("product id: "))
            except ValueError:
                print("That product id is not valid!")

        # Getting the product
        try:
            product = Product(**connector.get_product_information(product_id))
        except connector.TableNotFoundError as exc:
            raise AbortOperation("That product doesn't exist") from exc

        # Showing product information
        try:
            self.user.show_product_information(product)
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc

    def edit_product(self):
        '''
            Procedure for editing a product.
        '''

        # Asking for product id
        try:
            product_id = int(input("product id: "))
        except ValueError as exc:
            raise AbortOperation("product id is not valid!") from exc

        # Getting product
        try:
            product = Product(**connector.get_product_information(product_id))
        except connector.TableNotFoundError as exc:
            raise AbortOperation(f"the product with the id of {product_id} doesn't exist") from exc

        # Showing un-edited information of product
        try:
            self.user.show_product_information(product)
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc

        # Asking for new value
        print('Input new value for each attribute (Leave empty to not edit): ')
        name = input('Product name: ')
        name = None if name=='' else name
        category = input('Product category: ')
        category = None if category=='' else category
        description = input('Product description: ')
        description = None if description=='' else description
        try:
            price = input('Product price: ')
            if price != '':
                price = int(price)
                if price < 0:
                    raise AbortOperation("The product price can't be negative")
            else:
                price = None
        except ValueError:
            raise AbortOperation('The specified product price is invalid')

        # Editing product
        try:
            self.user.edit_product(product, name=name, category=category, description=description, price=price)
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc
        
        print(f'Product with the id of {product.product_id} has been edited')
        
    def delete_product_by_id(self):
        '''
            Procedure for deleting a product.
        '''

        # Asking for product id
        try:
            product_id = int(input("product id: "))
        except ValueError as exc:
            raise AbortOperation("product id is not valid!") from exc

        # Getting product
        try:
            product = Product(**connector.get_product_information(product_id))
        except connector.TableNotFoundError as exc:
            raise AbortOperation(f"the product with the id of {product_id} doesn't exist") from exc
        
        # Deleting product
        self.user.delete_product(product)
        print(f'Product with the id of {product.product_id} has been deleted')

    def show_transaction_by_id(self):
        '''
            Procedure for showing transaction information by its id
        '''

        # Asking for transaction id
        transaction_id = None
        while transaction_id is None:
            try:
                transaction_id = int(input("transaction id: "))
            except ValueError:
                print("That transaction id is not valid!")

        # Getting transaction
        try:
            transaction = Transaction(**connector.get_transaction_information(transaction_id))
        except connector.TableNotFoundError as exc:
            raise AbortOperation("That transaction doesn't exist") from exc
        
        # Showing transaction informations
        try:
            self.user.show_transaction_information(transaction)
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc
            
    def show_transactions(self):
        '''
            Print out transaction history.
        '''
        try:
            self.user.show_transaction_history()
        except PrivilegeError:
            print("You don't have the privilege to view transaction history")
    
    def do_transaction(self):
        '''
            Procedure for adding a new transaction
        '''

        # Asking for input
        transaction_type = input("Transaction type [IN/OUT/RETURN]: ")
        if transaction_type not in connector.TRANSACTIONS:
            raise AbortOperation('The specified type of transaction is not supported')

        receipt_number = input("receipt_number: ")
        receipt_number = None if receipt_number == '' else receipt_number

        try:
            num_of_product = int(input('Number of product: '))
            if num_of_product < 1:
                raise AbortOperation("The number of product can't be less than 1")
        except ValueError as exc:
            raise AbortOperation("The specified number of product is invalid") from exc

        # Asking for transaction details
        transaction_details = []
        for _ in range(num_of_product):
            try:
                product_id = int(input('Product id: '))
                if product_id < 1:
                    raise AbortOperation("Product id cannot be lower than 1")
            except ValueError as exc:
                raise AbortOperation("The specified product id is invalid") from exc

            product = Product(**connector.get_product_information(product_id))

            try:
                quantity = int(input('Quantity: '))
                if quantity < 1:
                    raise AbortOperation("Transaction quantity can't be less than 1")
            except ValueError as exc:
                raise AbortOperation(f"The specified quantity for product with the id of {product_id} is invalid") from exc
            transaction_details.append((product.product_id, quantity, product.price))

        # Adding new transaction
        try:
            new_transaction = self.user.do_transaction(receipt_number, transaction_details, transaction_type)
        except psycopg2.errors.ForeignKeyViolation as exc:
            raise AbortOperation(str(exc)) from exc
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc
        
        print(f"A new transaction of type {new_transaction.type} has been added with the id of {new_transaction.transaction_id} at {new_transaction.date_time}")

    def register(self):
        '''
            Procedure for registering a new employee.
        '''
        # Asking for input
        username = input('Username: ')
        username = None if username == '' else username
        password = getpass()
        password = None if password == '' else password
        name = input('Name: ')
        name = None if name == '' else name
        phone_number = input('Phone number: ')
        phone_number = None if phone_number == '' else phone_number
        address = input('Address: ')
        address = None if address == '' else address
        department = input('Department: ')
        department = None if department == '' else department
        if department not in connector.DEPARTMENTS:
            raise AbortOperation(f'There is no {department} department')

        # Registering new employee
        try:
            new_employee = self.user.register_account(username=username, password=password, name=name, phone_number=phone_number, address=address, department=department)
        except psycopg2.errors.UniqueViolation as exc:
            raise AbortOperation('That user already exists') from exc
        except psycopg2.errors.NotNullViolation as exc:
            raise AbortOperation(str(exc)) from exc
        except PrivilegeError as exc:
            raise AbortOperation(str(exc)) from exc


        print(f'User with the username {new_employee.get_username()} has been added with the id of {new_employee.get_employee_id()}')

    def select(self):
        '''
            Print and execute available menu selection
        '''

        # Creating selections
        if self.selections is None:
            self.selections = {
            'Show catalog' : self.show_catalog,
            'Show transactions' : self.show_transactions,
            'Show product by id' : self.show_product_by_id,
            'Show transaction by id' : self.show_transaction_by_id
            } 
            if isinstance(self.user, Can_Edit_Product_Info):
                self.selections.update(
                    {'Edit product by id': self.edit_product}
                )
            if isinstance(self.user, Can_Edit_Catalog):
                self.selections.update(
                    {
                        'Add new product': self.add_product,
                        'delete product by id': self.delete_product_by_id
                    }
                )
            if isinstance(self.user, Can_Do_Transaction):
                self.selections.update(
                    {'Do transaction' : self.do_transaction}
                )
            if isinstance(self.user, Management):
                self.selections.update(
                    {'Register user' : self.register}
                )
        
        print(f'Logged in as {self.user.get_name()} from {self.user.get_department()} department')

        # Printing available selections
        selection_list = list(self.selections)
        print("Procedures: ")
        for idx, selection in enumerate(selection_list, 1):
            print(f'{idx}. {selection}')

        # Asking for selection
        selected = None
        while selected is None:
            try:
                selected = int(input('Select procedure: ')) - 1
            except ValueError:
                print('Refer to the procedure by its number')

        os.system('cls')
        
        # Executing selected procedure
        selected = selection_list[selected]
        procedure = self.selections[selected]
        procedure()

if __name__ == '__main__':
    main()
