from datetime import datetime as time
import html_creator as creator

data = {"gold": "2",
        "silver": "1",
        "крест": "21",
        "образок": "22",
        "мощевик": "23",
        "кольцо": "24",
        "цепь": "25",
        "серьги": "27"}


def bill_number_add():
    file=open("num.counter", "r+")
    try:
        old_number = int(*file)
        new_number = old_number + 1
        file.seek(0)
        file.truncate()
        file.write(str(new_number))
        file.close()
        return new_number

    except:
        file.close()
        return {"message": "FILE ERROR"}


def bill_number_check():
    file = open("num.counter", "r+")
    try:
        number = int(*file)
        file.close()
        return number

    except:
        file.close()
        return {"message": "FILE ERROR"}


def bill_number_cleaner():
    file = open("num.counter", "r+")
    file.seek(0)
    file.truncate()
    file.close()


def customer_email(bill):
    order_dict = dict(bill)
    customer = order_dict.get("customer")
    email = str(customer["email"])

    return email


def customer_name(bill):
    order_dict = dict(bill)
    customer = order_dict.get("customer")
    name = str(customer["name"])

    return name


def article_compiler(bill):
    order_dict = dict(bill)
    customer = order_dict.get("customer")
    items_dict = order_dict.get("order")
    article = list()
    total = 0

    for item in items_dict:
        article_type = data.get(item["type"])
        article_material = data.get(item["material"])

        if int(item["count"]) == 1:
            result_price = int(item["price"])
        else:
            result_price = int(item["price"]) * int(item["count"])
        total = total + result_price

        text_material = 'Золото 585' if item["material"] == 'gold' else 'Серебро 725'

        article_result = (str(article_type) + str(article_material) + "." + str(item["article"]) + ".0"
                            + str(item["size"]) + "         " + str(item["type"]) + " " + str(item["name"]).upper()
                            + " (" + text_material + ") в количестве " + str(item["count"]) + " шт. "
                            + "(" + str(result_price) + " руб.)\n")

        article.append(article_result)

    bill_counter = bill_number_add()

    date = time.now()
    date_serialized = date.strftime("%d %m %Y - %H:%M:")

    result = ("Заказ № " + str(bill_counter) +" от " + str(date_serialized) +   "\n\nКлиент      ->      "
              + str(customer["name"]) + "\nПочта      ->      "
              + str(customer["email"]) + "\nТелефон для связи      ->      "
              + str(customer["number"]) + "\n\nКоментарий к заказу:\n"
              + '"' + str(customer["order_text"]) + '"'
              + "\n\nСписок изделий:\n\n" + str("".join(article))
              + "\nСумма заказа - " + str(total) + "р.")

    return result


def customer_compiler(bill):
    order_dict = dict(bill)
    items_dict = order_dict.get("order")
    customer = order_dict.get("customer")
    article = list()
    article_str = ""
    total = 0

    for item in items_dict:
        if int(item["count"]) == 1:
            result_price = int(item["price"])
        else:
            result_price = int(item["price"]) * int(item["count"])
        total = total + result_price

        material_as_text = 'Золото 585' if item["material"] == 'gold' else 'Серебро 725'


        result = ("<tr>" + creator.image_start + item["article"] + "_" + item["material"] + ".webp".replace('&#32;', '') + creator.image_end
                  + """<th align="left" style="color: #black;font-family: 'Tahoma', sans-serif;font-size: 13px;font-weight: normal;margin: 0;margin-bottom: 0px;margin-top: 0px;">"""
                  + str(item["type"]) + "<br>" + str(item["name"]).upper() +
                  """<br><p style="color: #696969;font-family: 'Tahoma', sans-serif;font-size: 11px;font-weight: normal;margin: 0;margin-bottom: 1px;">"""
                  + material_as_text + "</p></th>" + """<th align="center" style="color: #black;font-family: 'Tahoma', sans-serif;font-size: 13px;font-weight: normal;margin: 0;margin-bottom: 0px;margin-top: 0px;">"""
                  + str(item["count"]) + """</th><th style="color: #black;font-family: 'Tahoma', sans-serif;font-size: 13px;font-weight: normal;margin: 0;margin-bottom: 0px;margin-top: 0px;">"""
                  + str(item["price"]) + """ руб</th><th style="color: #black;font-family: 'Tahoma', sans-serif;font-size: 13px;font-weight: normal;margin: 0;margin-bottom: 0px;margin-top: 0px;">"""
                  + str(result_price) + " руб</th></tr>" + "\n")

        article.append(result)
        article_str = "".join(article)

    print(article_str)
    date = time.now()
    date_serialized = date.strftime("%d %m %Y")

    bill_counter = bill_number_check()

    result = (creator.body_1 + str(customer["name"]) + creator.body_2 + str(bill_counter) + creator.body_3
              + str(date_serialized) + creator.body_4 + str(customer["name"]) + creator.body_5 + str(article_str) + creator.body_6
              + str(total) + creator.body_7)

    print(result)
    total = 0
    return result


