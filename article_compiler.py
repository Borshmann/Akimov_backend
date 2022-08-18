from datetime import datetime as time

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
    total = 0

    for item in items_dict:
        if int(item["count"]) == 1:
            result_price = int(item["price"])
        else:
            result_price = int(item["price"]) * int(item["count"])
        total = total + result_price

        material_as_text = 'Золото 585' if item["material"] == 'gold' else 'Серебро 725'

        article_result = (str(item["type"]) + " " + str(item["name"]).upper()
                          + " (" + material_as_text + ") в количестве " + str(item["count"]) + " шт. "
                          + "(" + str(result_price) + " р.)\n")

        article.append(article_result)

    bill_counter = bill_number_check()

    date = time.now()
    date_serialized = date.strftime("%d %m %Y")

    result = ("Заказ № "+ str(bill_counter) + " от " + str(date_serialized) + "\n\n"
      + str(customer["name"]) + ", компания ООО 'АКИМОВ' благодарит за Ваш заказ! \nЗаказаные вами позиции:\n\n"
      + str("".join(article))
      + "\nСумма заказа - " + str(total) + "руб."+ "\n\nВ течении часа ожидайте звонка от нашего менеджера, чтобы уточнить все детали.\n\nСпасибо!")

    return result


