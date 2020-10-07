import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, item):
        """Добавляет элемент в список записей records.

        Parameters:
            item (Record): новая запись.
        """
        self.records.append(item)

    def get_today_stats(self):
        """Считает сколько единиц израсходавано сегодня.

        Returns:
            today_stats (int): сумма за текущий день.
        """
        now = dt.date.today()
        result = sum(item.amount for item in self.records
                     if item.date == now)
        return result

    def get_week_stats(self):
        """Считает сколько единиц израсходавано за последние 7 дней

        Returns:
            week_stats (int): сумма за последние 7 дней.
        """
        now = dt.date.today()
        start_period = now - dt.timedelta(days=7)
        result = sum(item.amount for item in self.records
                     if now >= item.date > start_period)
        return result

    def get_avaible_amount(self):
        """Вычисляет и возвращает доступный остаток на текущий день.

        Returns:
            avaible_amount (int): доступный остаток на текущий день.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня.

        Returns:
            calories_remained (str): сообщение о состоянии дневного баланса.
        """
        avaible_amount = self.get_avaible_amount()
        if avaible_amount > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {avaible_amount} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 78.17
    EURO_RATE = 92.12

    def get_today_cash_remained(self, currency):
        """Считает дневной баланс средств.

        Parameters:
            currency (str): строка, указывающая тип валюты (usd, eur, rub ...)

        Returns:
            today_cash_remained (str): сообщение о состоянии дневного баланса
        округленное до двух знаков после запятой (до сотых).
        """
        # Словарь хранит кортеж, в котором:
        # нулевой элемент - текстовое представление валюты
        # первый элемент - текущий курс конвертирования
        currency_convert = {
            'rub': ('руб', 1),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)
        }
        if currency not in currency_convert:
            raise ValueError('Это никогда не должно '
                             'произойти, но мы не '
                             'работаем с такой валютой')
        currency_, rate = currency_convert[currency]
        balance = self.get_avaible_amount()
        if balance != 0 and currency != 'rub':
            balance /= rate
        balance = round(balance, 2)
        if balance > 0:
            return f'На сегодня осталось {balance} {currency_}'
        if balance < 0:
            balance = -balance
            return f'Денег нет, держись: твой долг - {balance} {currency_}'
        return 'Денег нет, держись'


class Record:
    """Класс характеризующий записи.

    Parameters:
        amount (int): Величина (if defined),
        comment (str): Комментарий к записи (if defined),
        date (str): Дата записи (if defined).
    """

    def __init__(self, amount=0, comment='', date=None):
        self.amount = amount
        self.date = self.get_date(date)
        self.comment = comment

    def get_date(self, date):
        """Конвертер даты.
            Возвращает дату в формате date.

        Parameters:
            Тип date зависит от конструктора класса.
                date (str):  строка даты вида ДД.ММ.ГГГГ (if defined)

        Returns:
            date (datetime.date()): дата
        """
        if date is None:
            return dt.date.today()
        date_format = '%d.%m.%Y'
        return dt.datetime.strptime(date, date_format).date()
