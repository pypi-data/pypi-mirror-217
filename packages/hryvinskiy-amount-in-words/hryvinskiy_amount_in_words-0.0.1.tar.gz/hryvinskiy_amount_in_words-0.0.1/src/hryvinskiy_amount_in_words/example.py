#import decimal

units = {0: "", 1: "одна", 2: "дві", 3: "три", 4: "чотири", 5: "п'ять", 6: "шість", 7: "сім", 8: "вісім", 9: "дев'ять", 11: "одинадцять", 12: "дванадцять", 13: "тринадцять ", 14: "чотирнадцять", 15: "пʼятнадцять ", 16: "шістнадцять", 17: "сімнадцять", 18: "вісімнадцять", 19: "девʼятнадцять"}
tens = {0: "", 1:"десять", 2:"двадцять", 3:"тридцять", 4:"сорок", 5:"п'ятдесять", 6:"шістдесять" ,7:"сімдесять" ,8:"вісімдесять" ,9:"дев'яносто"}
hundreds = {0: "", 1:"сто" ,2:"двiстi" ,3:"триста" ,4:"чотириcта" ,5:"п'ятcот",6:"шiстсот",7:"ciмcот",8:"вiciмcот",9:"дев'ятсот"}

case_penny = {0: " копійок", 1:" копійка" ,2:" копійки" ,3:" копійки" ,4:" копійки" ,5:" копійок",6:" копійок",7:" копійок",8:" копійок",9:" копійок"}
case_hryvnia = {0: " гривень ", 1:" гривня " ,2:" гривні " ,3:" гривні " ,4:" гривні " ,5:" гривень ",6:" гривень ",7:" гривень ",8:" гривень ",9:" гривень "}
case_thousand = {0: " тисяч ", 1:" тисяча " ,2:" тисячі " ,3:" тисячі " ,4:" тисячі " ,5:" тисяч ",6:" тисяч ",7:" тисяч ",8:" тисяч ",9:" тисяч "}

def number_to_text(nam):
	number = nam#.quantize(decimal.Decimal('0.01'),rounding = decimal.ROUND_HALF_UP)

	namber_str = str(number)
	number_split = namber_str.split('.')

	if number < 1000000.00:
		integer_number = get_integer(number_split[0]).capitalize()
		hundredth_number = get_hundredth(number_split[1])

		if "  " in integer_number:
			integer_number = integer_number.replace("  ", " ")

		return integer_number + hundredth_number
	else:
		return "0 гривень 00 копійок, максимальне дозволене число '999999.99'\n"

def get_hundredth(number_str:str):
	return number_str + case_penny[int(number_str[1])]

def get_integer(number_str:str):
	if len(number_str) == 6:
		l0 = get_hundreds(int(number_str[0]),int(number_str[1]),int(number_str[2]))
		l1 = case_thousand[int(number_str[2])]

		l2 = get_hundreds(int(number_str[3]),int(number_str[4]),int(number_str[5]))
		l3 = case_hryvnia[int(number_str[5])]

		return l0 + l1 + l2 + l3

	elif len(number_str) == 5:
		l0 = get_tens(int(number_str[0]),int(number_str[1]))
		l1 = case_thousand[int(number_str[1])]

		l2 = get_hundreds(int(number_str[2]),int(number_str[3]),int(number_str[4]))
		l3 = case_hryvnia[int(number_str[4])]

		return l0 + l1 + l2 + l3

	elif len(number_str) == 4:
		l0 = get_units(int(number_str[0]))
		l1 = case_thousand[int(number_str[0])]

		l2 = get_hundreds(int(number_str[1]),int(number_str[2]),int(number_str[3]))
		l3 = case_hryvnia[int(number_str[3])]

		return l0 + l1 + l2 + l3

	elif len(number_str) == 3:
		l0 = get_hundreds(int(number_str[0]),int(number_str[1]),int(number_str[2]))
		l1 = case_hryvnia[int(number_str[2])]

		return l0 + l1

	elif len(number_str) == 2:
		l0 = get_tens(int(number_str[0]),int(number_str[1]))
		l1 = case_hryvnia[int(number_str[1])]

		return l0 + l1

	elif len(number_str) == 1:
		l0 = get_units(int(number_str[0]))
		l1 = case_hryvnia[int(number_str[0])]

		return l0 + l1

def get_units(number:int):
	return units[number]

def get_tens(number_0:int, number_1:int):
	number_str = str(number_0) + str(number_1)
	if int(number_str) in units.keys():
		return units[int(number_str)]
	else:
		return f"{tens[int(number_str[0])]} {units[int(number_str[1])]}"

def get_hundreds(number_0:int, number_1:int, number_2:int):
	if number_1 == 0 and number_2 == 0:
		return hundreds[number_0]
	elif number_1 == 1 and number_2 != 0:
		return f"{hundreds[number_0]} {get_tens(number_1, number_2)}"
	else:
		return f"{hundreds[number_0]} {tens[number_1]} {units[number_2]}"


"""if __name__ == "__main__":
	print("Привіт,я програма що перетворює числове представлення грошової суми в суму прописом.\nМаксимальне дозволене число '999999.99'\n")
	assert number_to_text(decimal.Decimal("1234.56")) == "Одна тисяча двiстi тридцять чотири гривні 56 копійок"
	while True:
		try:
			number = decimal.Decimal(input("Введіть суму: "))
			print("Результат:", number_to_text(number),"\n")
		except:
			print("Введіть суму числом\n")"""

		