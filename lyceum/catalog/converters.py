class MonthConverter:
    regex = r"[0-9]{1,2}"

    def to_python(self, value):
        if 1 <= int(value) <= 12:
            return int(value)
        else:
            raise ValueError("Номер месяца должен быть числом от 1 до 12")

    def to_url(self, value):
        return str(value)
