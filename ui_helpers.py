from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

def show_message(parent, title, message):
    QMessageBox.information(parent, title, message)

def show_warning(parent, title, message):
    QMessageBox.warning(parent, title, message)

def fill_table_with_products(table, products):
    table.setRowCount(len(products))
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['ID', 'Название', 'Количество'])

    for i, product in enumerate(products):
        table.setItem(i, 0, QTableWidgetItem(str(product[0])))
        table.setItem(i, 1, QTableWidgetItem(product[1]))
        table.setItem(i, 2, QTableWidgetItem(str(product[2])))

def fill_table_with_report(table, products):
    table.setRowCount(len(products))
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(['Продукт', 'Количество'])

    for i, product in enumerate(products):
        table.setItem(i, 0, QTableWidgetItem(product[1]))
        table.setItem(i, 1, QTableWidgetItem(str(product[2])))

def get_product_id_and_quantity(db, name, quantity_text):
    if not quantity_text:
        return None, None, 'Количество не может быть пустым'

    try:
        quantity = float(quantity_text)
    except ValueError:
        return None, None, 'Количество должно быть числом'

    product = db.get_product_by_name(name)
    if product:
        product_id, current_quantity = product
        return product_id, current_quantity, None
    else:
        return None, None, 'Продукт не найден'

def update_product_quantity_and_add_record(db, product_id, new_quantity, table, record_data):
    db.update_product_quantity(product_id, new_quantity)
    table.setRowCount(table.rowCount() + 1)
    row_position = table.rowCount() - 1

    for col, data in enumerate(record_data):
        table.setItem(row_position, col, QTableWidgetItem(str(data)))
