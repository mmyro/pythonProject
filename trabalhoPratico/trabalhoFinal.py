from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

root = Tk()

class Funcs():

    def limpa_tela(self):
        self.IdEntry.delete(0, END)
        self.nomeEntry.delete(0, END)
        self.idadeEntry.delete(0, END)
        self.telefoneEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        #self.espEntry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("dentista.bd")
        self.cursor = self.conn.cursor()
        print("Ligar a base de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desligar a base de dados")

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opcoes", menu=filemenu)
        filemenu.add_command(label="Sair", command=Quit)

    def contar_pac(self):
        self.conecta_bd()
        resultado = self.cursor.execute("select count(*) from pacientes").fetchone()
        self.desconecta_bd()
        return resultado[0]

    def submeterPaciente(self):
        id = self.idVal.get()
        nome = self.nomeVal.get()
        idade = self.idadeVal.get()
        telefone = self.telefoneVal.get()
        email = self.emailVal.get()

        if not nome or not idade or not email:
            messagebox.showerror('Erro', 'Por favor, preencha os campos', parent=root)
            return

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.limpa_tela()
            self.desconecta_bd()
            return

        strr = 'insert into pacientes (nome_paciente,idade,telefone,email) values(?,?,?,?)'
        self.cursor.execute(strr, (nome, idade, telefone, email))

        if self.cursor.rowcount == 1:
            self.conn.commit()
            messagebox.askyesnocancel('Notificações', 'Paciente {} adicionado'.format(nome), parent=root)
            self.select_lista()
        else:
            print("Error: Failed to insert data into the database.")
            messagebox.showerror('ERROR', parent=root)
            self.limpa_tela()

        self.desconecta_bd()

    def submeterDentista(self):
        nome = self.nomeVal.get()
        especializacao = self.espVal.get()

        if not nome or not especializacao:
            messagebox.showerror('Erro', 'Por favor, preencha os campos', parent=root)
            return

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.limpa_tela()
            self.desconecta_bd()
            return

        strr = 'insert into dentista (nome,especializacao) values (?,?)'
        self.cursor.execute(strr, (nome, especializacao))

        if self.cursor.rowcount == 1:
            self.conn.commit()
            messagebox.askyesnocancel('Notificações', 'Dentista {} adicionado'.format(nome), parent=root)
            self.select_lista()
        else:
            print("Error: Failed to insert data into the database.")
            messagebox.showerror('ERROR', parent=root)
            self.limpa_tela()

        self.desconecta_bd()

    def procurarPac(self):
        id = self.idVal.get()

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.desconecta_bd()
            return

        strr = 'select * from pacientes where cod = ?'
        self.cursor.execute(strr, (id,))
        result = self.cursor.fetchone()

        if result:
            self.idVal.set(result[0])
            self.nomeVal.set(result[1])
            self.idadeVal.set(result[2])
            self.telefoneVal.set(result[3])
            self.emailVal.set(result[4])
        else:
            messagebox.showerror('Erro', f'Paciente com ID {id} não encontrado', parent=root)

        self.desconecta_bd()

    def procurarDen(self):
        id = self.idVal.get()

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.desconecta_bd()
            return

        strr = 'select * from dentista where dentistaID = ?'
        self.cursor.execute(strr, (id,))
        result = self.cursor.fetchone()

        if result:
            self.idVal.set(result[0])
            self.nomeVal.set(result[1])
            self.espVal.set(result[2])
        else:
            messagebox.showerror('Erro', f'Dentista com ID {id} não encontrado', parent=root)

        self.desconecta_bd()

    def alterarPac(self):
        id_paciente = self.idVal.get()
        novo_nome = self.nomeVal.get()
        nova_idade = self.idadeVal.get()
        novo_telefone = self.telefoneVal.get()
        novo_email = self.emailVal.get()

        if not id_paciente:
            messagebox.showerror('Erro', 'Por favor, insira o ID do paciente', parent=self.root)
            return

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=self.root)
            self.desconecta_bd()
            return

        self.cursor.execute('SELECT * FROM pacientes WHERE cod = ?', (id_paciente,))
        resultado = self.cursor.fetchone()

        if resultado:
            self.cursor.execute(
                'UPDATE pacientes SET nome_paciente = ?, idade = ?, telefone = ?, email = ? WHERE cod = ?',
                (novo_nome, nova_idade, novo_telefone, novo_email, id_paciente))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Registro modificado com sucesso', parent=self.root)
            self.select_lista()
        else:
            messagebox.showerror('Erro', f'Paciente com ID {id_paciente} não encontrado', parent=self.root)

        self.desconecta_bd()

    def alterarDen(self):
        id_dentista = self.idVal.get()
        novo_nome = self.nomeVal.get()
        nova_esp = self.espVal.get()

        if not id_dentista:
            messagebox.showerror('Erro', 'Por favor, insira o ID do dentista', parent=self.root)
            return

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=self.root)
            self.desconecta_bd()
            return

        self.cursor.execute('SELECT * FROM dentista WHERE dentistaID = ?', (id_dentista,))
        resultado = self.cursor.fetchone()

        if resultado:
            self.cursor.execute(
                'UPDATE dentista SET nome = ?, especializacao = ? WHERE dentistaID = ?',
                (novo_nome, nova_esp, id_dentista))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Registro modificado com sucesso', parent=self.root)
            self.select_lista()
        else:
            messagebox.showerror('Erro', f'Dentista com ID {id_dentista} não encontrado', parent=self.root)

        self.desconecta_bd()

    def deletePac(self):
        id = self.idVal.get()

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.desconecta_bd()
            return

        strr = 'delete from pacientes where cod = ?'
        self.cursor.execute(strr, (id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            messagebox.showinfo('Sucesso', f'Paciente com ID {id} removido com sucesso', parent=root)
            self.select_lista()
        else:
            messagebox.showerror('Erro', f'Paciente com ID {id} não encontrado', parent=root)

        self.desconecta_bd()

    def deleteDen(self):
        id = self.idVal.get()

        self.conecta_bd()

        if self.cursor is None:
            print("Error: Unable to connect to the database.")
            messagebox.showerror('ERROR', parent=root)
            self.desconecta_bd()
            return

        strr = 'delete from dentista where dentistaID = ?'
        self.cursor.execute(strr, (id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            messagebox.showinfo('Sucesso', f'Dentista com ID {id} removido com sucesso', parent=root)
            self.select_lista()
        else:
            messagebox.showerror('Erro', f'Dentista com ID {id} não encontrado', parent=root)

        self.desconecta_bd()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT
    pacientes.cod AS cod,
    pacientes.nome_paciente AS nome_paciente,
    consulta.consultasID AS consultasID,
    consulta.dataConsulta AS dataConsulta,
    dentista.dentistaID AS dentistaID,
    dentista.nome AS nome_dentista
FROM
    consulta
JOIN pacientes ON consulta.consultasPacientesID = pacientes.cod
JOIN dentista ON consulta.consultasDentistaID = dentista.dentistaID;

 """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def addPaciente(self):
        self.conecta_bd()
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('400x250')
        self.root.title('Adicionar Paciente')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,borderwidth=3, width=10)
        self.nameLabel.place(x=20, y=20)
        self.idadeLabel = Label(self.root, text="Idade: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,borderwidth=3, width=10)
        self.idadeLabel.place(x=20, y=60)
        self.telefoneLabel = Label(self.root, text="Telefone: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,borderwidth=3, width=10)
        self.telefoneLabel.place(x=20, y=100)
        self.emailLabel = Label(self.root, text="Email: ", bg="#d3dbe0", font=('verdana', 14, 'bold'),relief=GROOVE, borderwidth=3, width=10)
        self.emailLabel.place(x=20, y=140)

        self.idVal = StringVar()
        self.nomeVal = StringVar()
        self.idadeVal = StringVar()
        self.telefoneVal = StringVar()
        self.emailVal = StringVar()

        self.nomeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=15)
        self.nomeEntry.place(x=170, y=20)
        self.idadeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idadeVal, width=15)
        self.idadeEntry.place(x=170, y=60)
        self.telefoneEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.telefoneVal, width=15)
        self.telefoneEntry.place(x=170, y=100)
        self.emailEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.emailVal, width=15)
        self.emailEntry.place(x=170, y=140)

        self.submitBtn = Button(self.root, text='Submeter', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.submeterPaciente)
        self.submitBtn.place(x=75, y=190)
        self.conn.commit()
        self.desconecta_bd()
        self.root.mainloop()

    def addDentista(self):
        self.conecta_bd()
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('470x170')
        self.root.title('Adicionar Dentista')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,borderwidth=3, width=15)
        self.nameLabel.place(x=20, y=20)
        self.idadeLabel = Label(self.root, text="Especializacao: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,borderwidth=3, width=15)
        self.idadeLabel.place(x=20, y=60)

        self.nomeVal = StringVar()
        self.espVal = StringVar()

        self.nomeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=15)
        self.nomeEntry.place(x=230, y=20)
        self.espEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.espVal, width=15)
        self.espEntry.place(x=230, y=60)

        self.submitBtn = Button(self.root, text='Submeter', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.submeterDentista)
        self.submitBtn.place(x=100, y=110)
        self.conn.commit()
        self.desconecta_bd()
        self.root.mainloop()

    def searchPaciente(self):
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('600x300')
        self.root.title('Procurar Paciente')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=10)
        self.idLabel.place(x=20, y=20)
        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                               borderwidth=3, width=10)
        self.nameLabel.place(x=20, y=60)
        self.idadeLabel = Label(self.root, text="Idade: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=10)
        self.idadeLabel.place(x=20, y=100)
        self.telefoneLabel = Label(self.root, text="Telefone: ", bg="#d3dbe0", font=('verdana', 14, 'bold'),
                                   relief=GROOVE, borderwidth=3, width=10)
        self.telefoneLabel.place(x=20, y=140)
        self.emailLabel = Label(self.root, text="Email: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=10)
        self.emailLabel.place(x=20, y=180)

        self.idVal = StringVar()
        self.nomeVal = StringVar()
        self.idadeVal = StringVar()
        self.telefoneVal = StringVar()
        self.emailVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=28)
        self.IdEntry.place(x=170, y=20)
        self.nomeEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=30)
        self.nomeEntry.place(x=170, y=60)
        self.idadeEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idadeVal, width=30)
        self.idadeEntry.place(x=170, y=100)
        self.telefoneEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.telefoneVal, width=30)
        self.telefoneEntry.place(x=170, y=140)
        self.emailEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.emailVal, width=30)
        self.emailEntry.place(x=170, y=180)

        self.submitBtn = Button(self.root, text='Procurar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.procurarPac)
        self.submitBtn.place(x=75, y=240)
        self.root.mainloop()

    def searchDentista(self):
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('525x200')
        self.root.title('Procurar Dentista')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=15)
        self.idLabel.place(x=20, y=20)
        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                               borderwidth=3, width=15)
        self.nameLabel.place(x=20, y=60)
        self.espLabel = Label(self.root, text="Especialização: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=15)
        self.espLabel.place(x=20, y=100)

        self.idVal = StringVar()
        self.nomeVal = StringVar()
        self.espVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=19)
        self.IdEntry.place(x=230, y=20)
        self.nomeEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=20)
        self.nomeEntry.place(x=230, y=60)
        self.espEntry = Label(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.espVal, width=20)
        self.espEntry.place(x=230, y=100)

        self.submitBtn = Button(self.root, text='Procurar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.procurarDen)
        self.submitBtn.place(x=130, y=140)
        self.root.mainloop()

    def updatePaciente(self):
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('400x300')
        self.root.title('Atualizar Paciente')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=10)
        self.idLabel.place(x=20, y=20)
        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                               borderwidth=3, width=10)
        self.nameLabel.place(x=20, y=60)
        self.idadeLabel = Label(self.root, text="Idade: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=10)
        self.idadeLabel.place(x=20, y=100)
        self.telefoneLabel = Label(self.root, text="Telefone: ", bg="#d3dbe0", font=('verdana', 14, 'bold'),
                                   relief=GROOVE, borderwidth=3, width=10)
        self.telefoneLabel.place(x=20, y=140)
        self.emailLabel = Label(self.root, text="Email: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=10)
        self.emailLabel.place(x=20, y=180)

        self.idVal = StringVar()
        self.nomeVal = StringVar()
        self.idadeVal = StringVar()
        self.telefoneVal = StringVar()
        self.emailVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=15)
        self.IdEntry.place(x=170, y=20)
        self.nomeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=15)
        self.nomeEntry.place(x=170, y=60)
        self.idadeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idadeVal, width=15)
        self.idadeEntry.place(x=170, y=100)
        self.telefoneEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.telefoneVal, width=15)
        self.telefoneEntry.place(x=170, y=140)
        self.emailEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.emailVal, width=15)
        self.emailEntry.place(x=170, y=180)

        self.submitBtn2 = Button(self.root, text='Procurar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=14,
                                command=self.procurarPac)
        self.submitBtn2.place(x=20, y=240)
        self.submitBtn = Button(self.root, text='Atualizar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=14,
                                command=self.alterarPac)
        self.submitBtn.place(x=200, y=240)
        self.root.mainloop()

    def updateDentista(self):
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('450x210')
        self.root.title('Atualizar Dentista')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=15)
        self.idLabel.place(x=20, y=20)
        self.nameLabel = Label(self.root, text="Nome: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                               borderwidth=3, width=15)
        self.nameLabel.place(x=20, y=60)
        self.espLabel = Label(self.root, text="Especialização: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                                borderwidth=3, width=15)
        self.espLabel.place(x=20, y=100)

        self.idVal = StringVar()
        self.nomeVal = StringVar()
        self.espVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=14)
        self.IdEntry.place(x=230, y=20)
        self.nomeEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.nomeVal, width=14)
        self.nomeEntry.place(x=230, y=60)
        self.espEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.espVal, width=14)
        self.espEntry.place(x=230, y=100)

        self.submitBtn2 = Button(self.root, text='Procurar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0",
                                 width=16,
                                 command=self.procurarDen)
        self.submitBtn2.place(x=20, y=150)
        self.submitBtn = Button(self.root, text='Atualizar', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0",
                                width=16,
                                command=self.alterarDen)
        self.submitBtn.place(x=230, y=150)
        self.root.mainloop()

    def deletePaciente(self):
        self.conecta_bd()
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('400x120')
        self.root.title('Eliminar Paciente')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=10)
        self.idLabel.place(x=20, y=20)

        self.idVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=15)
        self.IdEntry.place(x=170, y=20)
        self.submitBtn = Button(self.root, text='Submeter', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.deletePac)
        self.submitBtn.place(x=75, y=70)
        self.conn.commit()
        self.desconecta_bd()
        self.root.mainloop()

    def deleteDentista(self):
        self.conecta_bd()
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('400x120')
        self.root.title('Eliminar Dentista')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.idLabel = Label(self.root, text="Id: ", bg="#d3dbe0", font=('verdana', 14, 'bold'), relief=GROOVE,
                             borderwidth=3, width=10)
        self.idLabel.place(x=20, y=20)

        self.idVal = StringVar()
        self.IdEntry = Entry(self.root, font=('verdana', 14, 'bold'), bd=2, textvariable=self.idVal, width=15)
        self.IdEntry.place(x=170, y=20)
        self.submitBtn = Button(self.root, text='Submeter', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=20,
                                command=self.deleteDen)
        self.submitBtn.place(x=75, y=70)
        self.conn.commit()
        self.desconecta_bd()
        self.root.mainloop()

    def obter_pacientes(self):
        self.cursor.execute("SELECT nome_paciente FROM Pacientes")
        pacientes = [paciente[0] for paciente in self.cursor.fetchall()]
        return pacientes

    def obter_dentista(self):
        self.cursor.execute("SELECT nome FROM dentista")
        dentistas = [dentista[0] for dentista in self.cursor.fetchall()]
        return dentistas

    def obter_id_paciente(self, nome_paciente):
        self.conecta_bd()
        self.cursor.execute("SELECT cod FROM pacientes WHERE nome_paciente = ?", ( nome_paciente,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
        self.desconecta_bd()

    def obter_id_dentista(self, nome_dentista):
        self.conecta_bd()
        self.cursor.execute('SELECT dentistaID FROM dentista WHERE nome = ?', (nome_dentista,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
        self.desconecta_bd()

    def inserir_consulta(self):
        self.conecta_bd()
        paciente = self.varPaciente.get()
        dentista = self.var_dentista.get()
        data_consulta = self.EntryData.get()

        self.cursor.execute("SELECT COUNT(DISTINCT consultasID) AS total_ID FROM consulta;")
        resultado_encomendas = self.cursor.fetchone()

        paciente_id = self.obter_id_paciente(paciente)
        dentista_id = self.obter_id_dentista(dentista)

        if dentista_id is not None:
            id_encomenda = resultado_encomendas[0] + 1
            self.cursor.execute('INSERT INTO consulta (consultasID ,consultasPacientesID, consultasDentistaID, dataConsulta) VALUES (?, ?, ?, ?)',
                                (id_encomenda,paciente_id, dentista_id, data_consulta))
            self.conn.commit()

            mensagem = f"Consulta marcada para {data_consulta} com o paciente: {paciente} e o dentista: {dentista}."
            messagebox.showinfo("Consulta Agendada", mensagem)
        else:
            messagebox.showerror("Erro", f"Dentista {dentista} não encontrado.")
        self.select_lista()
        self.desconecta_bd()

    def novaConsulta(self):
        self.conecta_bd()
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.geometry('420x320')
        self.root.title('Nova Consulta')
        self.root.configure(background="#292930")
        self.root.resizable(FALSE, FALSE)

        self.welcome = Label(self.root, text="Nova Consulta",fg="white", bg="#292930" ,font=('verdana', 20, 'bold'))
        self.welcome.place(x=100, y=10)

        self.labelPaciente = Label(self.root, text="Escolha o Paciente:", fg="white", bg="#292930", font=('verdana', 14, 'bold'))
        self.labelPaciente.place(x=40, y=70)

        lista_pacientes = self.obter_pacientes()
        self.varPaciente.set(lista_pacientes[0])

        self.menuPaciente = OptionMenu(self.root, self.varPaciente, *lista_pacientes)
        self.menuPaciente.place(x=260, y=70)


        label_dentista = Label(self.root, text="Escolha o Dentista:", fg="white", bg="#292930", font=('verdana', 14, 'bold'))
        label_dentista.place(x=40, y=140)

        lista_dentistas = self.obter_dentista()
        self.var_dentista.set(lista_dentistas[0])

        # Menu suspenso para escolher dentista
        self.menu_dentista = OptionMenu(self.root, self.var_dentista, *lista_dentistas)
        self.menu_dentista.place(x=260, y=140)

        self.labelData = Label(self.root, text="Data da Consulta:", fg="white", bg="#292930", font=('verdana', 14, 'bold'))
        self.labelData.place(x=40, y=210)
        self.EntryData = Entry(self.root, bd="2",font=('verdana', 12, 'bold'), width=12)
        self.EntryData.place(x=250, y=215)

        self.inserirBtn = Button(self.root, text='Inserir', font=('verdanda', 14, 'bold'), bd=2, bg="#d3dbe0", width=15,
                                command=self.inserir_consulta)
        self.inserirBtn.place(x=110, y=260)

        self.desconecta_bd()
        self.root.mainloop()

    def mostrarPacientes(self):
        self.conecta_bd()
        pacientes_info = self.cursor.execute("SELECT * FROM pacientes").fetchall()
        self.desconecta_bd()

        janela = Toplevel()
        janela.title("Informações dos Pacientes")

        tree = ttk.Treeview(janela)
        tree["columns"] = ("ID", "Nome", "Idade", "Telefone", "Email")
        tree.heading("#0", text="")
        tree.column("#0", width=1, stretch=NO)
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Nome")
        tree.heading("#3", text="Idade")
        tree.heading("#4", text="Telefone")
        tree.heading("#5", text="Email")

        for info in pacientes_info:
            tree.insert("", END, values=info)

        tree.pack(expand=YES, fill=BOTH)

    def mostrarDentista(self):
        self.conecta_bd()
        dentistas_info = self.cursor.execute("SELECT * FROM dentista").fetchall()
        self.desconecta_bd()

        janela = Toplevel()
        janela.title("Informações dos Dentistas")

        tree = ttk.Treeview(janela)
        tree["columns"] = ("ID", "Nome", "Especializacao")
        tree.heading("#0", text="")
        tree.column("#0", width=1, stretch=NO)
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Nome")
        tree.heading("#3", text="Especializacao")

        for info in dentistas_info:
            tree.insert("", END, values=info)

        tree.pack(expand=YES, fill=BOTH)

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tabela()
        self.widgets_frame1()
        self.lista_frame2()
        self.Menus()
        self.select_lista()
        self.varPaciente = StringVar(self.root)
        self.var_dentista = StringVar(self.root)
        root.mainloop()

    def tela(self):
        self.root.title("Consultorio")
        self.root.configure(background='#292930')
        self.root.geometry('1300x700')
        self.root.resizable(True, True)
        self.root.maxsize(width=1500, height=900)
        self.root.minsize(width=400, height=400)

    def frames_da_tabela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = '#d3dbe0', borderwidth= 5)
        self.frame_1.place(relx = 0.02, rely = 0.13, relwidth = 0.4, relheight = 0.85)
        self.frame_2 = Frame(self.root, bd = 4, bg = '#d3dbe0', borderwidth=5)
        self.frame_2.place(relx = 0.45, rely = 0.13, relwidth = 0.53, relheight = 0.85)

    def widgets_frame1(self):
        self.lb_welcome = Label(self.root, font=('Helvetica', 30, 'italic bold'),text="Bem vindo", relief=RIDGE, borderwidth=5, width=15)
        self.lb_welcome.place(relx=0.35,rely=0)

        self.bt_novoPaciente = Button(self.frame_1, text="Novo Paciente", bd=2, bg='#292930', fg='white', font=('verdana', 12, 'bold'), command=self.addPaciente)
        self.bt_novoPaciente.place(relx=0.05, rely=0.02, relwidth=0.4, relheight=0.10)
        self.procurarPaciente = Button(self.frame_1, text="Procurar Paciente", bd=2, bg='#292930', fg='white', font=('verdana', 12, 'bold'), command=self.searchPaciente)
        self.procurarPaciente.place(relx=0.05, rely=0.16, relwidth=0.4, relheight=0.10)
        self.bt_alterarPaciente = Button(self.frame_1, text="Alterar Paciente", bd=2, bg='#292930', fg='white', font=('verdana', 12, 'bold'), command=self.updatePaciente)
        self.bt_alterarPaciente.place(relx=0.05, rely=0.3, relwidth=0.4, relheight=0.10)
        self.bt_apagarPaciente = Button(self.frame_1, text="Apagar Paciente", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.deletePaciente)
        self.bt_apagarPaciente.place(relx=0.05, rely=0.44, relwidth=0.4, relheight=0.10)

        self.bt_novaConsulta = Button(self.frame_1, text="Nova Consulta", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.novaConsulta)
        self.bt_novaConsulta.place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.10)

        self.bt_novoDentista = Button(self.frame_1, text="Novo Dentista", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.addDentista)
        self.bt_novoDentista.place(relx=0.55, rely=0.02, relwidth=0.4, relheight=0.10)
        self.procurarDentista = Button(self.frame_1, text="Procurar Dentista", bd=2, bg='#292930', fg='white', font=('verdana', 12, 'bold'), command=self.searchDentista)
        self.procurarDentista.place(relx=0.55, rely=0.16, relwidth=0.4, relheight=0.10)
        self.bt_alterarDentista = Button(self.frame_1, text="Alterar Dentista", bd=2, bg='#292930', fg='white', font=('verdana', 12, 'bold'), command=self.updateDentista)
        self.bt_alterarDentista.place(relx=0.55, rely=0.3, relwidth=0.4, relheight=0.10)
        self.bt_apagarDentista = Button(self.frame_1, text="Apagar Dentista", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.deleteDentista)
        self.bt_apagarDentista.place(relx=0.55, rely=0.44, relwidth=0.4, relheight=0.10)


        self.bt_tabelaPacientes = Button(self.frame_1, text="Tabela Pacientes", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.mostrarPacientes)
        self.bt_tabelaPacientes.place(relx=0.05,rely=0.74, relwidth=0.9, relheight=0.10)

        self.bt_tabelaDentista = Button(self.frame_1, text="Tabela Dentista", bd=2, bg='#292930', fg='white',font=('verdana', 12, 'bold'), command=self.mostrarDentista)
        self.bt_tabelaDentista.place(relx=0.05, rely=0.88, relwidth=0.9, relheight=0.10)

    def lista_frame2(self):
        scroll_x = Scrollbar(self.frame_2, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_2, orient=VERTICAL)
        self.listaCli = ttk.Treeview(self.frame_2, height=3,columns=("col1", "col2", "col3", "col4", "col5", "col6"))

        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Id")
        self.listaCli.heading("#2", text="Nome Paciente")
        self.listaCli.heading("#3", text="Id Consulta")
        self.listaCli.heading("#4", text="data")
        self.listaCli.heading("#5", text="Id Dentista")
        self.listaCli.heading("#6", text="Nome Dentista")


        self.listaCli.column("#0", width=1, stretch=NO)
        self.listaCli.column("#1", width=1)
        self.listaCli.column("#2", width=50)
        self.listaCli.column("#3", width=10)
        self.listaCli.column("#4", width=70)
        self.listaCli.column("#5", width=10)
        self.listaCli.column("#6", width=20)
        self.listaCli.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.95)


Application()