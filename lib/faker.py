from faker import Faker


class ZetsuBouFaker(Faker):
    def random_string(self, number: int = 8, is_lower: bool = False) -> str:
        s = "".join(self.random_letters(number))
        if is_lower:
            s = s.lower()
        return s

    def lower_name(self):
        return self.name().lower()
