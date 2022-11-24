def toString(expression):
    expression = expression.replace('[','').replace(']', '').replace(',','').replace("'", '').replace(' ', '')
    return expression