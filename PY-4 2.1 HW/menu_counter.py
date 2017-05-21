# coding: utf8
def csv_open():
	with open('list_of_dishes.txt', 'r', encoding = 'utf-8-sig') as f:
		# print(f.read())
		cook_book = {}
		for line in f:
			dish = line.strip().lower()
			count_ingridients = int(f.readline().strip())
			#print (count_ingridients)
			i = 0
			ingridients_list = []
			for i in range(count_ingridients):
				ingridient = f.readline().lower().split('|')
				ingridients = {}
				ingridients['ingridient_name'] = ingridient[0].strip()
				ingridients['quantity'] = int(ingridient[1].strip())
				ingridients['measure'] = ingridient[2].strip()
				#	{'ingridient_name': 'специи', 'quantity': 5, 'measure': 'гр.'}
				ingridients_list.append(ingridients)
			cook_book[dish] = ingridients_list
			f.readline()
	return cook_book
#print (csv_open())

def get_shop_list_by_dishes(dishes, person_count):
	shop_list = {}
	for dish in dishes:
		for ingridient in cook_book[dish]:
			new_shop_list_item = dict(ingridient)
			new_shop_list_item['quantity'] *= person_count
			if new_shop_list_item['ingridient_name'] not in shop_list:
				shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
			else:
				shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
	return shop_list

def print_shop_list(shop_list):
  for shop_list_item in shop_list.values():
    print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'],     shop_list_item['measure']))

def check_dish_in_cook_book(dishes):
	cook_book = csv_open()
	real_dishes = []
	for dish in dishes:
		if dish not in cook_book:
			continue
		else:
			real_dishes.append(dish)
	return real_dishes 

def create_shop_list():
	person_count = int(input('Введите количество человек: '))
	dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
	.lower().split(', ')
	real_dishes = check_dish_in_cook_book(dishes)
	if not real_dishes:
		print('Этих блюд в меню нет')
	elif len(real_dishes) < len(dishes):
		print('В меню только: {}'.format(', '.join(real_dishes)))
	else:
		shop_list = get_shop_list_by_dishes(real_dishes, person_count)
		print_shop_list(shop_list)

create_shop_list()


#print(check_dish_in_cook_book())