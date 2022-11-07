from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, emp_email, emp_password
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
def test_get_api_key_for_with_wrong_password(email=valid_email, password=invalid_password):
    """ Проверяем результат теста с правильным email и неправильным паролем. Ключ не должен быть в ответе."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

# 2 test
def test_get_api_key_with_wrong_email(email=invalid_email, password=invalid_password):
     """ Проверяем результат теста с неправильным email и правильным паролем. Ключ не должен быть в ответе."""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 3 test
def test_add_pet_long_name(name='Fedor', age='2', pet_photo='images/Fedor.jpg'):
    """Добавление питомца с названием породы из более 50 букв. Такой питомец не должен быть добавлен"""

    animal_type = 'ньюфаундлендротвейлеровчаркадогдолматинецчихуахуача'
    # 51 символ в названии породы

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 50, f'Добавлен питомец с длинным названием породы - {word_count} символов'

# 4 test
def test_get_list_of_pets_with_wrong_auth_key(filter='my_pets'):
    """ Проверяем что запрос списка питомцев с неверным auth_key выдаёт ошибку."""

    # Получаем ключ auth_key, портим его и запрашиваем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] += 'blah_blah_blah'
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Неверный auth_key' in result

# 5 test
def test_add_new_pet_with_letters_in_age(name='Мистер Ушастик', animal_type='кролик', age='Один',
                                     pet_photo='rabbit.jpg'):
    """Провереям что невозможно добавить питомца с буквенным значением возраста"""


    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['age'] == age

# 6 test
def test_add_new_pet_with_invalid_data(name='', animal_type='?)-%;',
                                     age='Сто', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'Введены некорректные данные' in result

# 7 test
def test_unsuccessful_delete_self_pet():
    """Проверяем возможность удаления питомца с некорректным ID"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Карамелька", "кошечка", "3", "images/candy.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id питомца, портим и отправляем на удаление
    pet_id = my_pets['pets'][0]['id']
    ID = pet_id['id'] += 'yahooo'
    status, _ = pf.delete_pet(auth_key, ID)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 403 и питомца удалит ьне удалось
    assert status == 403
    assert pet_id in my_pets.values()

# 8 test
