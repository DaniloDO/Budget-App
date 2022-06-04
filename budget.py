

class Category:

    def __init__(self, name):
        self.name = name
        self.total_funds = 0.0
        self.ledger = []

    def __repr__(self):
        string_object = f"{self.name:*^30}\n"
        total_amount = 0.00
        for item in self.ledger:
            while(len(item['description']) < 23):
                item['description'] += " "
            formatted_amount = '{:.2f}'.format(float(item['amount']))
            string_object += f"{item['description'][:23]:<21}{formatted_amount[:7]:>7}\n"
            total_amount += item['amount']
        string_object += f"Total: {total_amount:.2f}"

        return string_object

    def deposit(self, amount, description = ""):
        self.total_funds += amount
        add_ledger = {"amount": amount, "description": description}
        self.ledger.append(add_ledger)
        self.get_balance()

    def withdraw(self, amount, description = ""):
        allow_withdraw = self.check_funds(amount)
        if(allow_withdraw):
            self.total_funds -= amount
            add_ledger = {"amount": -amount, "description":description}
            self.ledger.append(add_ledger)
            self.get_balance()
            return True
        
        self.get_balance()
        return False

    def get_balance(self):
        return self.total_funds

    def transfer(self, amount, instance):
        allow_transfer = self.check_funds(amount)
        if(allow_transfer):
            self.withdraw(amount, f"Transfer to {instance.name}")
            instance.deposit(amount, f"Transfer from {self.name}")
            return True

        return False

    def check_funds(self, amount):
        if(amount > self.total_funds):
            return False

        return True

def create_spend_chart(categories):
    total_categories, percentages, name_categories = [], [], []
    total_withdraw = 0.00
    bar_line, vertical_name = "", ""

    #Calculates total value on each category and general
    for val in categories:
        total_category = 0
        for i in val.ledger:
            if(i["amount"] < 0):
                total_category += abs(i["amount"])

        total_categories.append(total_category)
        name_categories.append(val.name)

    total_withdraw = sum(total_categories)
      
    #Calculates percentages  
    for val in total_categories:
        percentages.append(round((val / total_withdraw) * 100, 2))
        truncated_percentages = list(map(lambda i: int(i/10) * 10, percentages))

    #Creates bar line
    for i in range(0, len(name_categories)):
        bar_line += ("-" * 3)
    bar_line += "-"

    #Creates class columns 
    name_mod = []
    max_len = max(list(map(lambda i: len(i), name_categories)))
    for val in name_categories:
        while(len(val) < max_len):
            val += " "
        name_mod.append(val)

    name_vertical = ""
    for i in range(0, max_len):
        name_vertical += (" " * 5)
        for j in range(0, len(name_mod)):
            name_vertical += name_mod[j][i] + (" " * 2)
        
        if(i < max_len - 1 or j < len(name_mod) -1):
            name_vertical += "\n"


    #Assemble Spending Chart
    spend_chart = f"Percentage spent by category\n"
    for i in range(100, -1, -10):
        spend_chart += f"{str(i)+'|':>4}"
        for j in range(0, len(truncated_percentages)):
            if(i > truncated_percentages[j]):
                spend_chart += "   "
            else:
                spend_chart += " o "

        spend_chart += " \n"
    
    spend_chart = f"{spend_chart}{bar_line:>{len(bar_line) + 4}}"

    spend_chart = f"{spend_chart}\n{name_vertical}"
  
    return spend_chart
  