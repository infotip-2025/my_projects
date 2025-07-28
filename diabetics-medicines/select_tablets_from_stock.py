def select_tablets(required_dose, stock):   
    # sorts stock dictionary by doses from lowest to highest
    stock = dict(sorted(stock.items()))

    # checks total available dosage
    available = sum([x*y for x, y in stock.items()])
    # ---- print(f'Available: {available}, required: {required_dose}')

    # create dictonary for our tablets composition,
    # with keys from stock and levels zeroed
    doses_composition = {x: 0 for x in stock.keys()}
    composed_dose_total = 0

    # returns the same stock levels and '0' if not emough left
    if available < required_dose:
        return (doses_composition, stock, 0)
    else:  # sufficient dosage in stock

        # takes doses from dictionary
        tablets_doses = list(stock.keys())
        # takes quantities of particular doses from dictionary
        tablets_quantities = list(stock.values())
        
        # ---- print(dict(zip(tablets_doses, tablets_quantities)))
        
        dose_to_add_index = 0
        dose_to_remove_index = 0
        
        while required_dose != composed_dose_total:
            # find the first/lowest available dose
            # ---- print(f'''dose_to_add_index {dose_to_add_index},
# ---- dose_to_remove_index {dose_to_remove_index},
# ---- tablets_doses[dose_to_add_index] {tablets_doses[dose_to_add_index]},
# ---- stock[tablets_doses[dose_to_add_index]] {stock[tablets_doses[dose_to_add_index]]}''')

            while stock[tablets_doses[dose_to_add_index]] == 0:
                dose_to_add_index += 1
            # add a tablet to my composition and remove it from stock    
            doses_composition[tablets_doses[dose_to_add_index]] += 1
            stock[tablets_doses[dose_to_add_index]] -= 1
            # count the composed dose
            composed_dose_total = \
                sum([x*y for x, y in doses_composition.items()])
            # if composed dose is over required dose
            # remove a piece of a lowest dose available
            # ---- print(f'required_dose {required_dose}, composed_dose_total {composed_dose_total}')
            while required_dose < composed_dose_total:
                # ---- print('!!! required_dose < composed_dose_total !!!')
                # find the first lowest dose available in composed tablet set
                while doses_composition[
                    tablets_doses[dose_to_remove_index]
                        ] == 0:
                    dose_to_remove_index += 1
                # add a tablet back to stock and remove it from my composition    
                doses_composition[tablets_doses[dose_to_remove_index]] -= 1
                stock[tablets_doses[dose_to_remove_index]] += 1
                # recalculate composed dose
                composed_dose_total = \
                    sum([x*y for x, y in doses_composition.items()])
                # ---- print(f'Had to remove a tablet - recalculated composed_dose_total: {composed_dose_total}')
        
        return (doses_composition, stock, 1)



stock_metformin = {
    #2000: 3,
    #1000: 3,
    #500: 1,
    5: 30,
    10: 2,
    20: 1,
    40: 3        
    }

stock_metformin = {
    5: 30,
    10: 5,
    20: 4,
    40: 5        
    }

x = select_tablets(2900, stock_metformin)
if x[2] != 1:
    print('no composition possible - not enough supplies')
else:
    print(f'composition: {x[0]},\nleft supplies: {x[1]}.')
# print(select_tablets(4000, stock_metformin))
