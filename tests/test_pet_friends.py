from api import PetFriends
from settings import valid_email, valid_password, password, email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#  10 tests more. 19.7.2

# 1 test
def add_pet_simple_with_valid_data(name='Candy_cat', animal_type='cat', age='5'):
    """Проверяем можно ли добавить питомца в упрощенном формате с корректными данными"""

#     Получаем api key  и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

#     Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# 2 test
def test_add_pet_photo_with_valid_data(pet_photo='candy.jpg'):
    """Проверим, что фото добавляется к конкретному питомцу"""

#     Получаем api key  и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
#     Получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

#     Проверяем есть ли в списке питомцы. Если список пустой,
#     добавляем питомца и запрашиваем список повторно.
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, 'Candy_cat simple', 'cat', '5')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

#     Берем ID первого в списке питомца и отправляем запрос на добавление фото.
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result

# 3 test
def add_pet_simple_with_invalid_data_symbol_in_age(name='Candy_cat', animal_type='cat', age='*&^%$#@!'):
    """Проверяем можно ли добавить питомца в упрощенном формате с некорректными данными - символы вместо чисел возраста"""

#     Получаем api key  и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

#     Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert 'Wrong data' in result

# 4 test
def test_get_api_key_with_wrong_password(email=valid_email, password=password):
    """ Проверяем результат теста с правильным email и неправильным паролем.
    Ключ не должен быть в ответе. Код ответа 403"""

    # Отправляем запрос, сохраняем ответы - status = статус код, result = текст ответа
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 403
    assert 'key' not in result

# 5 test
def test_get_api_key_with_wrong_data(email=email, password=password):
    """ Проверяем результат теста с неправильным email и неправильным паролем.
    Ключ не должен быть в ответе."""

    # Отправляем запрос, сохраняем ответы - status = статус код, result = текст ответа
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

# 6 test
def test_get_api_key_with_wrong_email(email=email, password=valid_password):
    """ Проверяем что запрос api ключа с неправильным email возвращает
    статус 403 и не содержит key"""

    # Отправляем запрос, сохраняем ответы - status = статус код, result = текст ответа
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 403
    assert 'key' not in result

# 7 test
def test_add_pet_long_type_name(name='Пушок', age='1', pet_photo='images/rabbit.jpg'):
    """Добавление питомца с названием породы из более 50 букв. Такой питомец не должен быть добавлен"""

    animal_type = 'ньюфаундлендротвейлеровчаркадогдолматинецчихуахуача'
    # 51 символ в названии породы

    # получаем auth key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # получаем список всех animal_type, считаем кол-во символов
    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 50, f'Добавлен питомец с длинным названием породы - {word_count} символов'

# 8 test
def test_get_list_of_pets_with_wrong_auth_key(filter='my_pets'):
    """ Проверяем что запрос списка питомцев с неверным auth_key выдаёт ошибку."""

    # Получаем ключ auth_key, портим его и запрашиваем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] += 'blah_blah_blah'
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Неверный auth_key' in result

# 9 test
def test_add_new_pet_with_empty_name_type(name='', animal_type='',
                                     age='1', pet_photo='cat1.jpg'):
    """Проверяем что нельзя добавить питомца с пустыми именем и animal_type"""

    # Получаем полный путь к jpg и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert 'БАГ - добавлен питомец без имени и породы' in result

# 10 test
def test_get_api_key_with_empty_email(email=' ', password=valid_password):
    """ Проверяем что запрос api ключа с пробелом в email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result
