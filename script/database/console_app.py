from getpass import getpass
import os

import psycopg2.errors

from table import Employee, Product, PrivilegeError
import connector
import auth

def main():
    menu = Menu()
    while True:
        print()
        try:
            menu.select()
        except AbortOperation as e:
            print(e)
        except KeyboardInterrupt:
            print("You have exited the console app")
            break

class AbortOperation(Exception):
    pass

class Menu:
    def __init__(self):
        user = None
        while not user:
            username = input("Username: ")
            password = getpass()
            user = auth.login(username, password)
            if not user:
                print("username or password is incorrect!")
                print()
        self.user = Employee(*user)

    def add_product(self):
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

        try:
            new_product = self.user.add_product(name=name, category=category, description=description, price=price)
        except PrivilegeError:
            print("You don't have the privilege to edit the catalog")
        except psycopg2.errors.NotNullViolation as exc:
            raise AbortOperation(str(exc)) from exc

        print(f"{new_product.name} has been added with the id of {new_product.product_id}")

    def show_catalog(self):
        self.user.show_catalog()

    def show_product_by_id(self):
        product_id = None
        while product_id is None:
            try:
                product_id = int(input("product id: "))
            except ValueError:
                print("That product id is not valid!")

        try:
            self.user.show_product_information(product_id)
        except connector.ProductNotFoundError as exc:
            raise AbortOperation("That product doesn't exist")

    def edit_product(self):
        try:
            product_id = int(input("product id: "))
        except ValueError as exc:
            raise AbortOperation("product id is not valid!") from exc

        try:
            self.user.show_product_information(product_id)
        except connector.ProductNotFoundError as exc:
            raise AbortOperation(f"the product with the id of {product_id} doesn't exist") from exc

        name = input('Product name: ')
        name = None if name=='' else name
        category = input('Product category: ')
        category = None if category=='' else category
        description = input('Product description: ')
        description = None if description=='' else description
        try:
            price = int(input('Product price: '))
            if price < 0:
                raise AbortOperation("The product price can't be negative")
        except ValueError:
            raise AbortOperation('The specified product price is invalid')


        self.user.edit_product(product_id, name, category, description, price)

    def show_transactions(self):
        try:
            self.user.show_transactions()
        except PrivilegeError:
            print("You don't have the privilege to view transaction history")

    def do_transaction(self):
        transaction_type = input("Transaction type [IN/OUT]: ")
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

        transaction_details = []
        for _ in range(num_of_product):
            try:
                product_id = int(input('Product id: '))
                if product_id < 1:
                    raise AbortOperation("Product id cannot be lower than 1")
            except ValueError as exc:
                raise AbortOperation("The specified product id is invalid") from exc

            try:
                quantity = int(input('Quantity: '))
                if quantity < 1:
                    raise AbortOperation("Transaction quantity can't be less than 1")
            except ValueError as exc:
                raise AbortOperation(f"The specified quantity for product with the id of {product_id} is invalid") from exc
            transaction_details.append((product_id, quantity))
        try:
            self.user.do_transaction(receipt_number, transaction_details, transaction_type)
        except psycopg2.errors.ForeignKeyViolation as exc:
            raise AbortOperation(str(exc)) from exc


    def register(self):
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

        try:
            new_employee = self.user.register_account(username=username, password=password, name=name, phone_number=phone_number, address=address, department=department)
        except psycopg2.errors.UniqueViolation as exc:
            raise AbortOperation('That user already exists') from exc
        except psycopg2.errors.NotNullViolation as exc:
            raise AbortOperation(str(exc)) from exc

        print(f'{new_employee.username} has been added with the id of {new_employee.get_employee_id()}')
            
    selections = {
        'Show catalog' : show_catalog,
        'Show product by id' : show_product_by_id,
        'Show transactions' : show_transactions,
        'Add new product': add_product,
        'Edit product by id': edit_product,
        'Do transaction' : do_transaction,
        'Register user' : register
    }

    def select(self):
        selection_list = list(self.selections)

        print("Procedures: ")
        for idx, selection in enumerate(selection_list, 1):
            print(f'{idx}. {selection}')

        selected = None
        while selected is None:
            try:
                selected = int(input('Select procedure: ')) - 1
            except ValueError:
                print('Refer to the procedure by its number')

        os.system('cls')
        
        selected = selection_list[selected]

        procedure = self.selections[selected]

        procedure(self)

if __name__ == '__main__':
    main()
