def semana_sort(dicionario):
    semana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']

    novo_dicionario = {}
    for i in range(0, 7):
        for dia, horarios in dicionario:
            if dia == semana[i]:
                novo_dicionario[dia] = horarios

    return novo_dicionario
