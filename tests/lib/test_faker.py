from lib.faker import ZetsuBouFaker


def test_random_datetime_str():
    faker = ZetsuBouFaker()

    for _ in range(20):
        date_str = faker.random_datetime_str()
        print(date_str)
