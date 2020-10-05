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
        now = dt.date.today()
        result = sum(item.amount for item in self.records
                     if item.date == now)
        return result

    def get_week_stats(self):
        """
        Считает сколько единиц израсходавано за последние 7 дней
        """
        now = dt.date.today()
        start_period = now - dt.timedelta(days=7)
        result = sum(item.amount for item in self.records
                     if now >= item.date >= start_period)
        return result

    def get_avaible_amount(self, today_balance, limit=None):
        """
        Принимает баланс текущего дня.
        Вычисляет и возвращает доступный остаток на текущий день.
        """
        if limit is None:
            return self.limit - today_balance
        return limit - today_balance


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """
        Определяет, сколько ещё калорий можно/нужно получить сегодня
        """
        today_balance = self.get_today_stats()
        if self.limit > today_balance:
            avaible_amount = self.get_avaible_amount(today_balance)
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
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
        # Словарь хранит кортеж, в котором:
        # нулевой элемент - текстовое представление валюты
        # первый элемент - текущий курс конвертирования
        currency_convert = {
            'rub': ('руб', 1),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)
        }
        today_balance = self.get_today_stats() / currency_convert[currency][1]
        limit = self.limit / currency_convert[currency][1]

        balance = round(self.get_avaible_amount(today_balance, limit), 2)
        currency = currency_convert[currency][0]
        if balance > 0:
            return f'На сегодня осталось {balance} {currency}'
        if balance < 0:
            balance = -balance
            return f'Денег нет, держись: твой долг - {balance} {currency}'
        return 'Денег нет, держись'


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
            return dt.date.today()
        date_format = '%d.%m.%Y'
        return dt.datetime.strptime(date, date_format).date()
