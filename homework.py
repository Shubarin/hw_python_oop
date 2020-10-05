import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, item):
        """
        Принимает на входе экземляр класса Record
        добавляет его в список записей records
        """
        self.records.append(item)

    def get_today_stats(self):
        """
        Считает сколько единиц израсходавано сегодня
        """
        result = 0
        now_date = dt.datetime.now().date()
        for item in self.records:
            if item.date == now_date:
                result += item.amount
        return result

    def get_week_stats(self):
        """
        Считает сколько единиц израсходавано за последние 7 дней
        """
        result = 0
        now_date = dt.datetime.now().date()
        for item in self.records:
            period = now_date - item.date
            if dt.timedelta(days=0) <= period < dt.timedelta(days=7):
                result += item.amount
        return result


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """
        Определяет, сколько ещё калорий можно/нужно получить сегодня
        """
        today_balance = self.get_today_stats()
        if self.limit > today_balance:
            avaible_amount = self.limit - today_balance
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {avaible_amount} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 78.17
    EURO_RATE = 92.12

    def get_today_cash_remained(self, currency):
        """
        принимает на вход код валюты: одну из строк "rub", "usd" или "eur".
        Возвращает сообщение о состоянии дневного баланса в этой валюте,
        округляя сумму до двух знаков после запятой (до сотых)
        """
        currency_translate = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        today_balance = self.get_today_stats()
        if currency == 'usd':
            today_balance = self.convert_usd_rub(today_balance)
            limit = self.convert_usd_rub(self.limit)
        elif currency == 'eur':
            today_balance = self.convert_eur_rub(today_balance)
            limit = self.convert_eur_rub(self.limit)
        else:
            limit = self.limit

        balance = round(limit - today_balance, 2)
        currency = currency_translate[currency]
        if balance > 0:
            return f'На сегодня осталось {balance} {currency}'
        if balance < 0:
            balance = -balance
            return f'Денег нет, держись: твой долг - {balance} {currency}'
        return 'Денег нет, держись'

    def convert_usd_rub(self, amount):
        """
        Принимает на вход сумму в долларах
        возвращает в рублях
        """
        return amount / CashCalculator.USD_RATE

    def convert_eur_rub(self, amount):
        """
        Принимает на вход сумму в евро
        возвращает в рублях
        """
        return amount / CashCalculator.EURO_RATE

    def convert_rub_usd(self, amount):
        """
        Принимает на вход сумму в рублях
        возвращает в долларах
        """
        return amount * CashCalculator.USD_RATE

    def convert_rub_eur(self, amount):
        """
        Принимает на вход сумму в рублях
        возвращает в евро
        """
        return amount * CashCalculator.EURO_RATE


class Record:
    """
    Класс характеризующий записи, принимает на вход три аргумента:
    amount - величина (по-умолчанию 0),
    comment - комментарий к записи (по-умолчанию - пустая строка (''),
    date - дата записи (по-умолчанию None, требуется обработка
    втроенным конвертором даты get_date(). Конвертация запускается
    при инициализации объекта.
    """

    def __init__(self, amount=0, comment='', date=None):
        self.amount = amount
        self.date = self.get_date(date)
        self.comment = comment

    def get_date(self, date):
        """
        Принимает на вход аргумент date, тип которого зависит от
        конструктора класса. Если в конструктор явно передали дату,
        то type(date) -> str будет преобразован в формат dt.datetime,
        и в таком виде будет возвращен в точку вызова.
        Если в конструктор явно не передавали дату, то метод вернет
        текущее состояние даты и времени dt.datetime.now()
        """
        if date is None:
            return dt.datetime.now().date()
        day, month, year = map(int, date.split('.'))
        return dt.datetime(year=year, month=month, day=day).date()
