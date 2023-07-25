import json
import pandas as pd

with open('trial_task.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Исходная таблица
extracted_data = pd.json_normalize(data)
# Разбираем отдельно products на таблицу
products_data = pd.json_normalize(data, record_path='products', meta='order_id', errors="ignore")

# Из исходной удаляем столбец, в котором продукты лежат списком
extracted_data.drop(['products'], axis='columns', inplace=True)

# Добавляем в исходную развернутые данные по продуктам
summary_data = extracted_data.merge(products_data, how='outer')

# TASK 1

# Группируем по id заказа и номеру склада и получаем сумму товаров в каждом заказе
group_data = summary_data.groupby(['order_id', 'warehouse_name', 'highway_cost'])['quantity'].sum().reset_index()

# Добавляем новый столбец со стоимостью доставки в каждом заказе
group_data['cost_delivery'] = (abs(group_data['highway_cost']) / group_data['quantity'])

# Группируем для вывода стоимости доставки по каждому складу
cost_delivery = group_data.groupby('warehouse_name')['cost_delivery'].mean().reset_index()
cost_delivery_renamed = cost_delivery.rename(
    columns={
        'warehouse_name': 'Склад',
        'cost_delivery': 'Стоимость доставки'
    }
)

print('Результат выполнения 1 задания: ')
print(cost_delivery_renamed)

# cost_delivery_renamed.to_excel('task_1.xlsx', sheet_name='data', index=True)

# TASK 2

# Делаем автономную копию DataFrame
summary_data_2 = summary_data.copy(deep=True)

full_table = pd.merge(summary_data_2, cost_delivery, how='inner')

# Добавляем столбцы:
# Доход
full_table['income'] = full_table['price'] * full_table['quantity']
# Расход
full_table['expenses'] = full_table['cost_delivery'] * full_table['quantity']
# Прибыль
full_table['profit'] = full_table['income'] - full_table['expenses']

group_products = full_table.groupby(['product'])[['quantity', 'income', 'expenses', 'profit']].sum().reset_index()

print('Результат выполнения 2 задания: ')
print(group_products)

# group_products.to_excel('task_2.xlsx', sheet_name='data', index=True)

# TASK 3

full_table_2 = full_table.copy(deep=True)
full_table_2 = full_table_2.sort_values(by='order_id')

group_orders = full_table_2.groupby(['order_id'])['profit'].sum().reset_index()
group_orders_renamed = group_orders.rename(
    columns={'profit': 'order_profit'}
)
print('Результат выполнения  3 задания: ')
print('Прибыль, полученная с заказов:')
print(group_orders_renamed)

# group_orders_renamed.to_excel('task_3.xlsx', sheet_name='data', index=True)

print('Средняя прибыль заказов:')
print(group_orders['profit'].mean())

# TASK 4

full_table_3 = full_table.copy(deep=True)
# Группируем по складам и проданным в них продуктам
group_warehouses = full_table_3.groupby(['warehouse_name', 'product'])[['quantity', 'profit']].sum().reset_index()
# Высчитываем прибыль по складам
warehouses_profit = group_warehouses.groupby(['warehouse_name'])['profit'].sum().reset_index()
# Переименовываем перед слиянием таблиц, т.к. в исходной уже есть столбец profit
warehouses_profit = warehouses_profit.rename(
    columns={'profit': 'warehouses_profit'}
)
# В сгруппированную таблицу добавляем прибыль склада для расчета процента товара от него
group_warehouses = pd.merge(group_warehouses, warehouses_profit, how='inner')
# Высчитываем процент прибыли продукта заказанного из определенного склада к прибыли этого склада
group_warehouses['percent_profit_product_of_warehouse'] = (group_warehouses['profit'] * 100) / group_warehouses[
    'warehouses_profit']

print('Результат выполнения 4 задания: ')
print(group_warehouses)

# group_warehouses.to_excel('task_4.xlsx', sheet_name='data', index=True)

# TASK 5

group_warehouses_sort = group_warehouses.copy(deep=True)
# сортировка по убыванию
group_warehouses_sort = group_warehouses_sort.sort_values(['warehouse_name', 'percent_profit_product_of_warehouse'],
                                                          ascending=[True, False])
# добавление столбца накопленного процента
group_warehouses_sort['accumulated_percent_profit_product_of_warehouse'] = \
    group_warehouses_sort.groupby('warehouse_name')['percent_profit_product_of_warehouse'].cumsum()

print('Результат выполнения 5 задания: ')
print(group_warehouses_sort)

# group_warehouses_sort.to_excel('task_5.xlsx', sheet_name='data', index=True)


# TASK 6

# Создаем функцию для определения категорий
def category(row):
    if row['accumulated_percent_profit_product_of_warehouse'] <= 70:
        return 'A'
    elif 70 < row['accumulated_percent_profit_product_of_warehouse'] <= 90:
        return 'B'
    else:
        return 'C'


category_table = group_warehouses_sort.copy(deep=True)

# Применяем функцию для столбца с помощью метода apply()
category_table['category'] = category_table.apply(category, axis=1)

print('Результат выполнения 6 задания: ')
print(category_table)

# category_table.to_excel('task_6.xlsx', sheet_name='data', index=True)
