import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from cf_test import my_pets

# Поиск всех питомцев пользователя
def test_get_list(my_pets):

    WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    stat = int(pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text.split()[2])

    WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    assert stat == len(pets)


# Тест на наличие фото у питомцев
def test_pet_photo(my_pets):

    WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    stat = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    number_of_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_photos += 1

    print(f'Количество фото: {number_of_photos}')

# Тест заполненности полей "имя", "возраст", "порода"
def test_filled_fields(my_pets):

    pytest.driver.implicitly_wait(5)

    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result == 3

# Тест на отсутствие одинаковых имён у питомцев
def test_all_pets_have_different_names(my_pets):

    WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])

    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(r)
    print(pets_name)

# Тест на отсутствие одинаковых питомцев
def test_no_duplicate_pets(my_pets):
    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    pytest.driver.implicitly_wait(5)
    breeds = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    pytest.driver.implicitly_wait(5)
    ages = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

    pets = []
    r = 0
    print()

    for i in range(len(names)):

        pets.append({
            'name': names[i].text,
            'breed': breeds[i].text,
            'age': ages[i].text
        })

        print('pets[', str(i), ']=', pets[i])


        r = pets.count(pets[i])
        print('количество =', str(r))
        if r != 1:
            break

    assert r == 1