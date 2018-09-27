from pyspark.sql import SQLContext
from pyspark import SparkContext
import re
import sys

"""
    run me throught ${SPARK_DIRECTORY}/bin/spark-submit
    you can use > to redirect my output, to be more easily read:
    spark-submit find_anomalies.py path/data_dump.csv 2> err.txt
"""

def check_member(member):
	reg = "\A10\d{4}\Z"
	if not(re.match(reg, str(member))):
		return False
	return True

def check_date(date):
	reg="(200[0-9]|201[0-7])-(0\d|1[0-2])-(0\d|[12]\d|3[0-1])"
	if not(re.match(reg, date)):
		return False
	# Feb and bisextile years
	res = re.match("(....)-02-(..)", date)
	if (res):
		year = int(res.group(1))
		day = int(res.group(2))
		if (day > 29 or (day==29 and year%4!=0)):
			return False
	return True

def check_country(country):
	#list from https://datahub.io/fr/dataset/iso-3166-1-alpha-2-country-codes/resource/9c3b30dd-f5f3-4bbe-a3cb-d7b2c21d66ce
	#we added XK, which is sometime used for kosovo
	all_country_code = ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW","XK"]
	if country in all_country_code:
		return True
	else:
		return False

def check_gender(gender):
	reg = "(Male|Female)$"
	if not(re.match(reg, gender)):
		return False
	return True

def check_ip_adr(adr):
	reg = "\A(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\Z"
	bytes = re.match(reg, adr)
	isValid = True
	for i in range(1,5):
		tmpbyte = bytes.group(i)
		#many values use 255 and 0 so they must be legit
		isValid = isValid and (int(tmpbyte) <= 255) and (int(tmpbyte) >= 0)
	return isValid

def check_amount(amount):
	reg = "\A\$\d{3,4}\.\d{2}\Z$"
	if re.match(reg, amount):
		return True
	else:
		return False

def check_vip(vip):
	reg = "\A(true|false)\Z"
	if re.match(reg, str(vip)):
		return True
	else:
		return False

def check_product_id(product_id):
	#peut on faire mieux? FIXME
	#is it usefull to perform check if it is already an int?
	reg = "\A330\d{3}\Z"
	if re.match(reg, str(product_id)):
		return True
	else:
		return False

def check_card_type(card_type):
	#utiliser la question sur les types de cartes pour completer cette partie
	reg = "americanexpress|bankcard|china-unionpay|diners-club-carte-blanche|diners-club-enroute|diners-club-international|diners-club-us-ca|instapayment|jcb|laser|maestro|mastercard|solo|switch|visa|visa-electron"
	if re.match(reg, card_type):
		return True
	else:
		return False

def check_serial(serial):
	reg = "\d{3}-\d{2}-\d{4}$"
	if re.match(reg, serial):
		return True
	else:
		return False

def check_zone(zone):
	reg = "zone[1-7]$"
	if re.match(reg, zone):
		return True
	else:
		return False


def check_entry(entry):
	#result = check_member(entry.member_id) comment tester un int?
	#result = result and check_date(entry.date) comment tester une date?
	result = check_country(entry.country)
	result = result and check_gender(entry.gender)
	result = result and check_ip_adr(entry.ip_address)
	result = result and check_amount(entry.amount)
	result = result and check_date(entry.date)
	result = result and check_member(entry.member_id)
	result = result and check_vip(entry.vip)
	result = result and check_product_id(entry.product_id)
	result = result and check_card_type(entry.card_type)
	result = result and check_serial(entry.serial)
	result = result and check_zone(entry.zone)
	return result

def produce_list(entry):
	if not check_entry(entry):
		return [entry]
	else:
		return []

def createTuple(customer):
	s = set()
	s.add(customer.gender)
	return (customer.member_id, s)

if (len(sys.argv)<2):
	print("Argument 1: Nom du fichier input")
	exit(1)
input_path = sys.argv[1]
	
if __name__ == "__main__":
    spark = SparkContext.getOrCreate()
    sqlContext = SQLContext(spark)
    df = sqlContext.read.load(input_path,
            format='com.databricks.spark.csv',
            header='true')
    anormal_data = df.rdd.map(lambda customer: produce_list(customer)).reduce(lambda a,b : a+b)
    print ("anomalies trouvees : %i" % len(anormal_data))
    print('\n'.join(map(str, anormal_data)))
