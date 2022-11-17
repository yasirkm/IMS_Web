from getpass import getpass

from table import Employee, Product
import connector
import auth

def main():
    # user = Employee(1, 'eric', 'hahaha', 'Eric Nur', '08122121212', 'Bandung', 'Management')
    # new_user = Employee(0, 'yasirkm', 'hohoho', 'Yasir Khairul', '081122334455', 'Bandung', 'Management')
    # user.register_account(new_user)

    # new_product = Product(0, 'produk baru', 'futuristic', 2203, 'produk untuk testing')
    # user.show_catalog()
    # user.add_product(new_product)
    # user.show_catalog()
    
    # product1 = Product(*connector.get_product_information(user, 1))

    # user.show_product_information(1)
    # user.edit_product(product1, name='ini baru diupdate')
    # user.show_product_information(1)
    # user.edit_product(product1, name='pillow')

    # user.show_transactions()
    # user.show_product_information(1)
    # user.do_transaction(None, ((product1, 5),), "IN")
    # user.show_transactions()
    # user.show_product_information(1)

    menu = Menu()
    while True:
        print()
        try:
            menu.select()

        except AbortOperation as e:
            print(e)
        except KeyboardInterrupt:
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
        category = input('Product category: ')
        description = input('Product description: ')
        price = int(input('Product price: '))

        new_product = Product(0, name, category, price, 0, description)

        self.user.add_product(new_product)

    def show_catalog(self):
        self.user.show_catalog()

    def show_product_by_id(self):
        product_id = None
        while not product_id:
            try:
                product_id = int(input("product id: "))
            except ValueError:
                print("That product id is not valid!")

        self.user.show_product_information(product_id)

    def edit_product(self):
        product_id = None
        while not product_id:
            try:
                product_id = int(input("product id: "))
            except ValueError:
                detail = "product id is not valid!"
                raise AbortOperation(detail)

        self.user.show_product_information(product_id)
        try:
            product = Product(*connector.get_product_information(self.user, product_id))
        except TypeError:
            detail = "Product not found"
            raise AbortOperation(detail)


        name = input('Product name: ')
        category = input('Product category: ')
        description = input('Product description: ')
        price = int(input('Product price: '))

        self.user.edit_product(product, name, category, description, price)

    def show_transactions(self):
        self.user.show_transactions()

    def do_transaction(self):
        pass

    def register(self):
        username = input('Username: ')
        password = getpass()
        name = input('Name')
        phone_number = input('Phone number: ')
        address = input('Address: ')
        department = input('Department')

        params = (username, password, name, phone_number, address, department)
        params = (value if value!='' else None for value in params)

        new_account = Employee(*params)
        self.user.register_account(new_account)

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
        
        selected = selection_list[selected]

        procedure = self.selections[selected]

        procedure(self)

if __name__ == '__main__':
    main()
