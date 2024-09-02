from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date

import tkinter as tk
from tkinter import messagebox

from view import bar_valores, pie_valores, percentagem_valor, inserir_categoria, ver_categoria, inserir_receita, inserir_gastos, tabela, deletar_gastos, deletar_receitas

co1 = "#1a1919"
co4 = "#61e786"
co9 = "#272d2d"

colors = ['#5588bb', '#66bbbb', '#99bb55', '#eee994', '#444466', '#bb5555']
text_color = '#ffffff'

janela = Tk()
janela.title("Orçamento Pessoal")
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

# Personalizar estilo da Treeview
style.configure("Treeview",
                background="#1a1919",
                foreground="white",
                fieldbackground="#1a1919",
                rowheight=25,
                borderwidth=0)
style.configure("Treeview.Heading",
                background="#1a1919",
                foreground="white",
                font=('Verdana', 10))

# Personalizar estilo da Scrollbar
style.configure("Vertical.TScrollbar",
                gripcount=0,
                background="#1a1919",
                troughcolor="#333",
                bordercolor="#333",
                arrowcolor="#fff",
                sliderlength=20,
                sliderrelief="flat")

style.configure("Horizontal.TScrollbar",
                gripcount=0,
                background="#444",
                troughcolor="#333",
                bordercolor="#333",
                arrowcolor="#fff",
                sliderlength=20,
                sliderrelief="flat")


frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=co1,pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)


app_img = Image.open('CH-imagoh-VB.png')
app_img = app_img.resize((170,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" Orçamento pessoal", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana', 20, 'bold'), bg=co1, fg=co4,)
app_logo.place(x=0, y=0)

global tree

def inserir_categoria_b():
    nome = e_categoria.get().strip()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_categoria.delete(0, 'end')

    categoria_funcao = ver_categoria()
    categoria = []

    for i in categoria_funcao:
        categoria.append(i[1])

    combo_categoria_despesas['values'] = (categoria)

def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receitas.get().strip()
    quantia = e_valor_receitas.get().strip()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return 
        
    inserir_receita(lista_inserir)   

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso') 

    e_categoria.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

def inserir_gastos_b():
    nome = combo_categoria_despesas.get().strip()
    data = e_cal_despesas.get().strip()
    quantia = e_valor_despesas.get().strip()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=="":
            print("Chegou no ponto da mensagem")
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return 

    inserir_gastos(lista_inserir)

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso') 

    combo_categoria_despesas.delete(0,'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')   
        

    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome =='Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()
    except IndexError:
            messagebox.showinfo('Erro', 'Selecione um dos dados da tabela')

def percentagem():
    l_nome = Label(frameMeio, text="Porcentagem de Receita restante", height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#61e786')
    style.configure("TProgressbar", thickness=25)
    
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = percentagem_valor()[0]

    valor = percentagem_valor()[0]

    l_percentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_percentagem.place(x=200, y=35)

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    figura = plt.Figure(figsize=(4, 3.45), dpi=60, facecolor='#1a1919')
    ax = figura.add_subplot(111)

    ax.bar(lista_categorias, lista_valores, color=colors, width=0.9)

    c = 0

    for i in ax.patches:
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic', verticalalignment='bottom', color='#ffffff')
        c += 1

    ax.set_xticks(range(len(lista_categorias)))
    ax.set_xticklabels(lista_categorias, fontsize=16, color=text_color)

    ax.tick_params(axis='y', labelcolor='#ffffff')


    ax.patch.set_facecolor('#1a1919')
    ax.spines['bottom'].set_color('#cccccc')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#eeeeee')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

def resumo():
    valor = bar_valores()

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario= Label(frameMeio, text="Total Renda Mensal                     ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83e9e6')
    l_sumario.place(x=309, y=35)
    l_sumario= Label(frameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=70)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)
    l_sumario= Label(frameMeio, text="Total Despesas Mensais                  ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83e9e6')
    l_sumario.place(x=309, y=115)
    l_sumario= Label(frameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)
    l_sumario= Label(frameMeio, text="Total Saldo da Conta                    ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83e9e6')
    l_sumario.place(x=309, y=190)
    l_sumario= Label(frameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)

frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co1)
frame_gra_pie.place(x=415, y=5)

def grafico_pie():
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    figura.patch.set_facecolor(co1)

    ax = figura.add_subplot(111)
    ax.set_facecolor(co1)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0 ]


    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90, textprops={'color': '#ffffff'})
    legend=ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))
    legend.get_frame().set_facecolor('#1a1919')
    legend.get_frame().set_edgecolor('#1a1919')

    for text in legend.get_texts():
        text.set_color('#ffffff')

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

percentagem()
grafico_bar()
resumo()
grafico_pie()

frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2, padx=5)



app_tabela = Label(frameMeio, text=" Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4,)
app_tabela.place(x=5, y=309)




def mostrar_renda():
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()
    
    global tree

    style.configure("Treeview",
                    background="#1a1919",
                    foreground="white",
                    fieldbackground="#1a1919",
                    rowheight=25,
                    borderwidth=0)
    style.configure("Treeview.Heading",
                    background="#1a1919",
                    foreground="white",
                    font=('Verdana', 10))

    # Configurar estilo da Scrollbar
    style.configure("Vertical.TScrollbar",
                    gripcount=0,
                    background="#444",
                    troughcolor="#333",
                    bordercolor="#333",
                    arrowcolor="#fff",
                    sliderlength=20,
                    sliderrelief="flat")

    style.configure("Horizontal.TScrollbar",
                    gripcount=0,
                    background="#444",
                    troughcolor="#333",
                    bordercolor="#333",
                    arrowcolor="#fff",
                    sliderlength=20,
                    sliderrelief="flat")

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1


    for item in lista_itens:
        tree.insert('', 'end', values=item, tags=('numeric',))

    tree.tag_configure('numeric', foreground='#ffffff')


l_info = Label(frame_operacoes, text='Insira novas despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_categoria = Label(frame_operacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

categoria_funcao = ver_categoria()
categoria = []


for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=110, y=41)


l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_despesas.place(x=110, y=71)


l_valor_despesas = Label(frame_operacoes, text='Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)


img_add_despesas = Image.open('plus.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, command=inserir_gastos_b, image=img_add_despesas, text=" Adicionar".upper(), width=80, compound=LEFT, relief=RAISED, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co4, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)


l_excluir = Label(frame_operacoes, text='Excluir ação', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)

img_delete = Image.open('close.png')
img_delete = img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, command=deletar_dados, image=img_delete, text=" Deletar".upper(), width=80, compound=LEFT, relief=RAISED, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co4, overrelief=RIDGE)
botao_deletar.place(x=110, y=190)





l_info = Label(frame_configuracao, text='Insira novas receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_cal_receitas = Label(frame_configuracao, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas= DateEntry(frame_configuracao, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_receitas.place(x=110, y=41)

l_valor_receitas = Label(frame_configuracao, text='Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110, y=71)

img_add_receitas = Image.open('/Users/henriquehida/Documents/P_Finance/plus.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao,command=inserir_categoria_b, image=img_add_receitas, text=" Adicionar".upper(), width=80, compound=LEFT, relief=RAISED, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co4, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=111)




l_info = Label(frame_configuracao, text='Categoria', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=160)

e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y=160)

img_add_categoria = Image.open('/Users/henriquehida/Documents/P_Finance/plus.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_configuracao, command=inserir_categoria_b, image=img_add_categoria, text=" Adicionar".upper(), width=80, compound=LEFT, relief=RAISED, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co4, overrelief=RIDGE)
botao_inserir_categoria.place(x=110, y=190)


mostrar_renda()


janela.mainloop()
