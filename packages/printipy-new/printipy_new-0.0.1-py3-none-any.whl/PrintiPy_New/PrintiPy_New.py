import base64
import requests
import os
import cv2 as cv
from time import sleep


api_token = ''
shop_id = ''


class Product:
    def __init__(self, data):
        self.raw_data = data
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.tags = data['tags']
        self.options = data['options']
        self.variants = data['variants']
        self.images = data['images']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.visible = data['visible']
        self.is_locked = data['is_locked']
        self.blueprint_id = data['blueprint_id']
        self.user_id = data['user_id']
        self.shop_id = data['shop_id']
        self.print_provider_id = data['print_provider_id']
        self.print_areas = data['print_areas']


class Upload:
    def __init__(self, data):
        self.raw_data = data
        self.id = data['id']
        self.file_name = data['file_name']
        self.height = data['height']
        self.width = data['width']
        self.size = data['size']
        self.mime_type = data['mime_type']
        self.preview_url = data['preview_url']
        self.upload_time = data['upload_time']


def set_token(token:str):
    global api_token
    api_token = token


def set_shop_id(id:str):
    global shop_id
    shop_id = id


def get_request(url:str, header:dict=dict(), data:dict=dict()) -> requests.Response:
    return requests.get(f'https://api.printify.com/v1/{url}', headers={'Authorization': f'Bearer {api_token}'} | header, json=data)


def post_request(url:str, header:dict=dict(), data:dict=dict()) -> requests.Response:
    return requests.post(f'https://api.printify.com/v1/{url}', headers={'Authorization': f'Bearer {api_token}'} | header, json=data)


def put_request(url:str, header:dict=dict(), data:dict=dict()) -> requests.Response:
    return requests.put(f'https://api.printify.com/v1/{url}', headers={'Authorization': f'Bearer {api_token}'} | header, json=data)


def request_is_successful(re:requests.Response) -> bool:
    if re.status_code < 200 or re.status_code >= 300:
        is_successful = False
    else:
        is_successful = True

    return is_successful


def __print_status(name:str, re:requests.Response):
    print(name, 'status:', re.status_code, '\n')


def __invalid_request(re:requests.Response) -> Exception:
    print(re.json())
    return Exception(f'Request is invalid. Status code {re.status_code}')


def convert_data(url:str) -> str:

    with open(url, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        f.close()

    return data


def compress_data(url:str) -> str:

    image = cv.imread(url)

    data = base64.b64encode(cv.imencode('.jpg', image, [int(cv.IMWRITE_JPEG_QUALITY), 100])[1].tobytes()).decode('utf-8')

    return data


def connect(print_status=True):

    re = get_request('shops.json')    

    if print_status:
        __print_status(connect.__name__, re)

    for shop in re.json():
        print(shop
              )
    print('')


def get_product(product_id:str, print_status=True) -> Product:

    re = get_request(f'shops/{shop_id}/products/{product_id}.json')

    if print_status:
        __print_status(get_product.__name__, re)

    return Product(re.json())


def get_products_list(limit=100, page=1, print_status=True) -> list:

    if limit > 100:
        raise Exception('Maximum limit is 100.')
    elif limit < 1:
        raise Exception('Minimum limit is 1.')

    products = []

    re = get_request(f'shops/{shop_id}/products.json', data={'limit': f'{limit}', 'page': f'{page}'})

    if request_is_successful(re):
        for value in re.json()['data']:
            products.append(Product(value))
    
        if print_status:
            __print_status(get_products_list.__name__, re)

        return products

    else:
        raise __invalid_request(re)


def get_upload(upload_id:str, print_status=True) -> Upload:

    re = get_request(f'uploads/{upload_id}.json')

    if print_status:
        __print_status(get_upload.__name__, re)

    return Upload(re.json())


def get_uploads_list(limit=100, page=1, print_status=True) -> list:

    if limit > 100:
        raise Exception('Maximum limit is 100.')
    elif limit < 1:
        raise Exception('Minimum limit is 1.')

    uploads = []

    re = get_request('uploads.json', data={'limit': f'{limit}', 'page': f'{page}'})
    
    if request_is_successful(re):
        for value in re.json()['data']:
            uploads.append(Upload(value))

        if print_status:
            __print_status(get_uploads_list.__name__, re)

        return uploads

    else:
        raise __invalid_request(re)


def upload_image(url:str, print_status=True, print_response=False) -> Upload:

    url = url.replace('\\', '/')

    file_name_index = 0

    if '/' in url:
        file_name_index = url.rindex('/')+1

    file_name = url[file_name_index:]

    if 'http://' in url or 'https://' in url:
        re = post_request('uploads/images.json', data={'file_name': file_name, 'url': url})

    elif os.path.exists(url):
        re = post_request('uploads/images.json', data={'file_name': file_name, 'contents': convert_data(url)})

        if not request_is_successful(re):
            re = post_request('uploads/images.json', data={'file_name': file_name, 'contents': compress_data(url)})

    else:
        raise Exception('File/URL does not exist.')

    if request_is_successful(re):
        if print_status:
            __print_status(upload_image.__name__, re)

        return Upload(re.json())

    else:
        raise __invalid_request(re)


def copy_product(product:Product, title='', description='', print_status=True) -> Product:
    og_title = product.title
    og_description = product.description

    blueprint_id = product.blueprint_id
    print_provider_id = product.print_provider_id

    variants = product.variants
    print_areas = product.print_areas

    data = {}

    if title == '':
        data |= {'title': f'Copy {og_title}'}
    else:
        data |= {'title': title}

    if description == '':
        data |= {'description': og_description}
    else:
        data |= {'description': description}

    data |= {'blueprint_id': blueprint_id, 'print_provider_id': print_provider_id, 'variants': variants, 'print_areas': print_areas}

    re = post_request(f'shops/{shop_id}/products.json', data=data)

    if request_is_successful(re):
        if print_status:
            __print_status(copy_product.__name__, re)

        return Product(re.json())

    else:
        raise __invalid_request(re)


def update_product(product_id:str, title='', description='', tags=[], image_id='', print_area_index=0, print_status=True) -> Product:

    product_data = get_product(product_id).raw_data

    if title != '':
        product_data['title'] = title

    if description != '':
        product_data['description'] = description
    
    if tags != []:
        product_data['tags'] = tags

    if image_id != '':
        product_data['print_areas'][print_area_index]['placeholders'][0]['images'][0]['id'] = image_id

    re = put_request(f'shops/{shop_id}/products/{product_id}.json', data=product_data)

    if request_is_successful(re):
        if print_status:
            __print_status(update_product.__name__, re)

        return Product(re.json())

    else:
        raise __invalid_request(re)


def update_product_raw_data(product_id:str, product_data:dict(), print_status=True) -> Product:

    re = put_request(f'shops/{shop_id}/products/{product_id}.json', data=product_data)

    if request_is_successful(re):
        if print_status:
            __print_status(update_product_raw_data.__name__, re)

        return Product(re.json())

    else:
        raise __invalid_request(re)


def publish_product(product_id:str, print_status=True):

    re = post_request(f'shops/{shop_id}/products/{product_id}/publish.json', 
                      data={'title': True,
                            'description': True,
                            'images': True,
                            'variants': True,
                            'tags': True,
                            'keyFeatures': True,
                            'shipping_template': True})

    if request_is_successful(re):
        if print_status:
            __print_status(publish_product.__name__, re)

    else:
        raise __invalid_request(re)


def create_new_product_from_copy(product:Product, image_url:str, publish=False, title='', description='', tags=[], print_area_index=0, print_status=True):
    
    image = upload_image(image_url)
    new_product = copy_product(product)

    update_product(new_product.id, title, description, tags, image.id, print_area_index=0)

    if publish:
        publish_product(new_product.id)