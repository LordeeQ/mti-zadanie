class Formatter:

    # 1250000 -> "1 250 000 руб."
    @staticmethod
    def price(value):
        return f"{value:,}".replace(",", " ") + " руб."

    @staticmethod
    def stock(in_stock):
        if in_stock:
            return "В наличии"
        return "Продан"
