from table import Employee, Product
import connector

def main():
    user = Employee(1, 'eric', 'hahaha', 'Eric Nur', '08122121212', 'Bandung', 'Management')
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



if __name__ == '__main__':
    main()
