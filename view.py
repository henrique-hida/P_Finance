import sqlite3 as lite
import pandas as pd

con = lite.connect("dados.db")

def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i)

def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)

def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)



def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)


def ver_categoria():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


def ver_receitas():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

def ver_gastos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista

def bar_valores():
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
            gastos_lista.append(i[3])

    gasto_total = sum(gastos_lista)

    saldo_total = receita_total - gasto_total

    return [receita_total,gasto_total,saldo_total]


def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns = ['id', 'categoria', 'Data', 'valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append (i)

    return([lista_categorias, lista_quantias])


def percentagem_valor():
    receitas = ver_receitas()
    receitas_lista = [i[3] for i in receitas]
    receita_total = sum(receitas_lista)
    
    gastos = ver_gastos()
    gastos_lista = [i[3] for i in gastos]
    gasto_total = sum(gastos_lista)
    
    if receita_total == 0:
        return [0]

    total = ((receita_total - gasto_total) / receita_total) * 100
    
    return [total]
