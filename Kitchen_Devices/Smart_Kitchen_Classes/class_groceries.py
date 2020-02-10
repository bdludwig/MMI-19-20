# groceries beschreibt alle Lebensmittel.
# name = Name; date_buy = Kaufsdatum; amount = Wie oft das selbe?; size = Größe der Portion
# category = Kategorie (Fleisch, Fisch, Gemüse, ...); allergen = Allergene

class groceries:
    def __init__(self, name, date_buy, amount, size, category, allergen):
        self.name = name
        self.date_buy = date_buy
        self.amount = amount
        self.size = size
        self.category = category
        self.allergen = allergen


class perishable(groceries):
    def __init__(self, name, date_buy, amount, size, category, allergen, expiry):
        groceries.__init__(self, name, date_buy, amount, size, category, allergen)
        self.expiry = expiry


class nonPerishable(groceries):
    def __init__(self, name, date_buy, amount, size, category, allergen):
        groceries.__init__(self, name, date_buy, amount, size, category, allergen)


class spice(groceries):
    def __init__(self, name, date_buy, amount, size, category, allergen):
        groceries.__init__(self, name, date_buy, amount, size, category, allergen)
