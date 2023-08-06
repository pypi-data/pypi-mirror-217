def classes_numericas(n: int) -> str:
    if isinstance(n, float) or isinstance(n, str):
        return """
        =========================================================
        |   Por favor, digite um valor numérico inteiro         |
        |   que seja menor do que um quattuordecilhão,          |
        |   pois trato apenas até a casa dos tredecilhões.      |
        =========================================================
        Ass.: rene (͠≖ ͜ʖ͠≖)👌

        (obs: não gostou, faça o seu código...) (¬‿¬)
        """
    if n == 0:
        return '0'
    if n > 999999999999999999999999999999999999999999999:
        return """
        =================================================
        |   Por favor, digite um valor menor do que     |
        |   um quattuordecilhão, pois trato apenas      |
        |   até a casa dos tredecilhões.                |
        =================================================
        Ass.: rene (͠≖ ͜ʖ͠≖)👌

        (obs: não gostou, faça o seu código...) (¬‿¬)
        """

    n = [i for i in str(n)]
    clas = [' unidade', ' dezena', ' centena']
    clas_mil = ['', ' de milhar', ' de milhão', ' de bilhão', ' de trilhão', ' de quadrilhão', ' de quintilhão', ' de sextilhão', ' de setilhão', ' de octilhão', ' de nonilhão', ' de decilhão', ' de undecilhão', ' de duodecilhão', ' de tredecilhão']

    count_mil = 0

    pos = 0
    neg = -1
    while True:
        if pos == len(clas):
            pos = 0
        
        if int(n[neg]) > 1:
            n[neg] += clas[pos] + 's' + clas_mil[count_mil]
        elif int(n[neg]) == 0:
            pass
        else:
            n[neg] += clas[pos] + clas_mil[count_mil]

        if neg*(-1) == len(n):
            break
        
        if neg*(-1) % 3 == 0:
            count_mil += 1

        pos += 1
        neg -= 1

    classes_num = [i for i in n if i != '0']
    classes_num[-1] = ' e ' + classes_num[-1] if len(classes_num) > 1 else classes_num[-1]
    result = ', '.join(classes_num[:-1]) + classes_num[-1]

    return result

if __name__ == "__main__":
    while True:
        n = int(input('>>>\t'))
        print(classes_numericas(n))
