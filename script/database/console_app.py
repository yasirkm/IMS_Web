from table import Employee, Product
import connector

def main():
    user = Employee(1, 'eric', 'hahaha', 'Eric Nur', '08122121212', 'Bandung', 'Management')
    # new_product = Product(0, 'produk baru', 'futuristic', 2203, 'produk untuk testing')
    # user.show_catalog()
    # user.add_product(new_product)
    # user.show_catalog()
    
    # user.show_product_information(1)
    # user.edit_product(1, name='ini baru diupdate')
    # user.show_product_information(1)
    # user.edit_product(1, name='pillow')

    product1 = Product(1, *connector.get_product_information(user, 1))
    user.show_transactions()
    user.show_product_information(1)
    user.do_transaction(None, ((product1, 5),), "IN")
    user.show_transactions()
    user.show_product_information(1)

if __name__ == '__main__':
    main()
