import requests
from xml.etree import ElementTree

# from topsdk.client import TopApiClient, TopException

req_provider = requests.get('http://stripmag.ru/datafeed/p5s_full_stock.xml')
req_feed = requests.get('http://alitair.1gb.ru/Intim_Ali_allfids_2.xml')

root_provider = ElementTree.fromstring(req_provider.text)
root_feed = ElementTree.fromstring(req_feed.text)


# Функция обработки данных от поставщика.
# Возвращает словарь, содержащий id товаров со значениями в виде словаря с данными о товаре.
def get_new_data(root):
    data = {}

    for product in root:
        product_id = product.attrib['prodID']
        quantity = product[1][0].attrib['sklad']
        price = product[0].attrib['BaseRetailPrice']

        data[product_id] = {'quantity': quantity, 'price': price}

    return data


# Обновление фита.
def feet_update():
    provider_data = get_new_data(root_provider)

    # Обновление фита.
    for offer in root_feed.iter('offer'):
        if offer.attrib['id'] in provider_data:
            offer.find('price').text = provider_data[offer.attrib['id']]['price']
            offer.find('quantity').text = provider_data[offer.attrib['id']]['quantity']


# Обновление остатков и цен маркетплейса.
def marketplace_update():
    # Авторизация для запроса.
    client = TopApiClient(appkey='<your-appkey>',
                          app_sercet='<your-appsecret>',
                          top_gateway_url='<top-gateway-url>',
                          verify_ssl=False)

    # Обновление остатков и цен.
    for offer in root_feed.iter('offer'):
        multiple_sku_update_list_price = []
        multiple_sku_update_list_inventory = []
        if 'ae_intim4_id' in offer.attrib:
            multiple_sku_update_list_price.append({"price": offer.find('price').text})

            request_dict_price = {
                "product_id": offer.attrib['ae_intim4_id'],
                "multiple_sku_update_list": multiple_sku_update_list_price
            }

            # Изменение цены.
            try:
                response = client.execute_with_session("aliexpress.solution.batch.product.price.update",
                                                       request_dict_price,
                                                       "<user-session>")
                print(response)
            except TopException as e:
                print(e)

            multiple_sku_update_list_inventory.append({"inventory": offer.find('quantity').text})

            request_dict_price = {
                "product_id": offer.attrib['ae_intim4_id'],
                "multiple_sku_update_list": multiple_sku_update_list_inventory
            }

            # Изменение остатков.
            try:
                response = client.execute_with_session("aliexpress.solution.batch.product.inventory.update",
                                                       request_dict,
                                                       "<user-session>")
                print(response)
            except TopException as e:
                print(e)


feet_update()
marketplace_update()
