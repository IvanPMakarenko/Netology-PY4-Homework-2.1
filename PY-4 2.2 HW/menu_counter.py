# coding: utf8
#pip3 install pyyaml
import json
import yaml
import csv
import xml.etree.ElementTree as ET
from pprint import pprint

def txt_open():
	with open('list_of_dishes.txt', 'r', encoding = 'utf-8-sig') as f:
		cook_book = {}
		for line in f:
			dish = line.strip().lower()
			count_ingridients = int(f.readline().strip())
			ingridients_list = []
			for _i in range(count_ingridients):
				ingridient = f.readline().lower().split('|')
				ingridients = {}
				ingridients['ingridient_name'] = ingridient[0].strip()
				ingridients['quantity'] = int(ingridient[1].strip())
				ingridients['measure'] = ingridient[2].strip()
				ingridients_list.append(ingridients)
			cook_book[dish] = ingridients_list
			f.readline()
	return cook_book
#pprint (txt_open())

def json_loader():
	
	with open('list_of_dishes_json.json', encoding = 'utf-8') as f:
		json_book = json.load(f)
		return json_book

#json_loader()


def yaml_loader():
	with open('list_of_dishes_yaml.yml', encoding = 'utf-8') as yaml_file:
		yaml_book = yaml.load(yaml_file)
		return yaml_book

#yaml_loader()

def data_parser(function):
	data_book = function
	cook_book = {}
	for dishes in data_book:
		cook_book[dishes['dish']] = dishes['ingridients']
	return cook_book

#data_parser()

def csv_open():
	with open('list_of_dishes_csv.csv', encoding='utf8') as csvfile:
		csv_menu = csv.DictReader(csvfile, delimiter=';')
		csv_list = []
		for row_for_dishes in csv_menu:
			csv_list.append(row_for_dishes)
		csv_book = {}
		ingridients_list = []
		fix_list = []
		for data in csv_list:
			csv_book[data['dish']]=None
		for dish in csv_book:
			ingridients_list = []
			for data in csv_list:
				if dish == data['dish']:
					ingridients = {}
					ingridients['ingridient_name'] = data['ingridient_name'].strip()
					ingridients['quantity'] = int(data['quantity'].strip())
					ingridients['measure'] = data['measure'].strip()
					ingridients_list.append(ingridients)
					csv_book[data['dish']] = ingridients_list
				else:
					continue
		return csv_book

#csv_open()

def file_type():
	user_needs = input('Введите тип файла (yaml, json, txt, csv): ')
	if user_needs == 'yaml':
		return data_parser(yaml_loader())
	if user_needs == 'json':
		return data_parser(json_loader())
	if user_needs == 'txt':
		return txt_open()
	if user_needs == 'csv':
		return csv_open()

#pprint(file_type())


def get_shop_list_by_dishes(dishes, person_count, final_cook_book):
	shop_list = {}
	for dish in dishes:
		for ingridient in final_cook_book[dish]:
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

def check_dish_in_cook_book(dishes, final_cook_book):
	cook_book = final_cook_book
	real_dishes = []
	for dish in dishes:
		if dish not in cook_book:
			continue
		else:
			real_dishes.append(dish)
	return real_dishes 

def create_shop_list():
	final_cook_book = file_type()
	person_count = int(input('Введите количество человек: '))
	dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
	.lower().split(', ')
	real_dishes = check_dish_in_cook_book(dishes, final_cook_book)
	if not real_dishes:
		print('Этих блюд в меню нет')
	elif len(real_dishes) < len(dishes):
		print('В меню только: {}'.format(', '.join(real_dishes)))
		short_shop_list = get_shop_list_by_dishes(real_dishes, person_count, final_cook_book)
		print_shop_list(short_shop_list)
	else:
		shop_list = get_shop_list_by_dishes(real_dishes, person_count, final_cook_book)
		print_shop_list(shop_list)

create_shop_list()


#Далее идут мои попытки по парсингу xml. У меня не получилось выбирать лишь первые N ингридиентов, которые принадлежат одному блюду. Только последнее блюдо верно записывается..
# tree = ET.parse('list_of_dishes_xml.xml')
# xml_book = {}

# for row in tree.iter():
# 	#print(row.tag, row.attrib, row.text)
# 	if row.tag == 'dish':
# 		xml_book[row.attrib['name']] = None
# #print(xml_book)
# for dishes in xml_book:
# 	#print(dishes)
# 	ingridients = []
# 	for row in tree.iter():
# 		if row.tag == 'dish' and row.attrib['name'] == dishes:
# 			ingridients = []
# 		elif row.tag == 'ingridient':
# 			ingridients.append(row.attrib)
# 			xml_book[dishes] = ingridients
# 			#print(xml_book)

# pprint(xml_book)
