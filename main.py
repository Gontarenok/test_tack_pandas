import json
import pandas as pd

# data = pd.read_json('trial_task.json')
# print(data)

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
group_data = summary_data.groupby(['order_id', 'warehouse_name', 'highway_cost'])['quantity'].sum()

# Превращаем объект выборки обратно в DataFrame
group_data = group_data.reset_index()

# Добавляем новый столбец со стоимостью доставки в каждом заказе
group_data['cost_delivery'] = (abs(group_data['highway_cost']) / group_data['quantity'])

# Группируем для вывода стоимости доставки по каждому складу
cost_delivery = group_data.groupby('warehouse_name')['cost_delivery'].mean()
cost_delivery = cost_delivery.reset_index()
cost_delivery_renamed = cost_delivery.rename(
    columns={
        'warehouse_name': 'Склад',
        'cost_delivery': 'Стоимость доставки'
    }
)
print(cost_delivery_renamed)

# TASK 2

summary_data_2 = summary_data.copy(deep=True)

full_table = pd.merge(summary_data_2, cost_delivery, how='inner')
# print(full_table)
group_products = full_table.groupby(['product', 'price', 'cost_delivery'])['quantity'].sum().reset_index()


# Доход
group_products['income'] = group_products['price'] * group_products['quantity']
# Расход
group_products['expenses'] = group_products['cost_delivery'] * group_products['quantity']
# Прибыль
group_products['profit'] = group_products['income'] - group_products['expenses']

group_products = group_products.groupby(['product'])[['quantity', 'income', 'expenses', 'profit']].sum().reset_index()

print(group_products)

# group_products = full_table.groupby(['product'])[('quantity', 'income', 'expenses', 'profit')].sum()
# print(group_products)

# result_table = pd.DataFrame()
# result_table['product'] = full_table['product']
# # суммарное количество
# result_table['quantity'] = full_table['quantity']
# # суммарный доход
# result_table['income'] = full_table['quantity']
# # суммарный расход
# result_table['expenses'] = full_table['quantity']
# # суммарная прибыль
# result_table['profit'] = full_table['quantity']
# print(result_table)




# summary_data.to_excel('summary_data_2.xlsx', sheet_name='data', index=True)

# print(data.tail(10))
# print(data.dtypes)
# print(data[['order_id', 'products']])

# data.to_excel('data.xlsx', sheet_name='data', index=False)

# data_mordor = data[data['warehouse_name'] == 'Мордор']
# print(data_mordor)

# data_mordor = data.loc[data['warehouse_name'] == 'Мордор', 'highway_cost']
# print(data_mordor)

# data['highway_cost'].plot()
# plt.show()


# print(data['products'].describe())
