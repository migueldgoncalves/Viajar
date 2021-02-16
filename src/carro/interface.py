import tkinter as tk
import math


class InterfaceTkinter:

    angulo = 0  # Graus
    window = None
    canvas = None
    linha = None

    def __init__(self):

        InterfaceTkinter.window = tk.Tk()
        # A espessura do limite deve ser no mínimo 1 para se usar o atributo "relief"
        '''frm_a = tk.Frame(relief=tk.RIDGE, borderwidth=5)
        frm_a.pack(fill=tk.BOTH)
        frm_b = tk.Frame()
        frm_b.pack()
        lbl_hi = tk.Label(text="Hiii", foreground="red", background="yellow", width=10, height=10, master=frm_b)
        lbl_hi.pack(side=tk.LEFT)
        btn = tk.Button(text="Algo", fg="yellow", bg="white", width=20, height=20, master=frm_b)
        btn.pack(side=tk.LEFT)
        ent = tk.Entry(text="Insert here", master=frm_b)
        ent.pack(side=tk.LEFT)
        txt = tk.Text(width=30, height=20, master=frm_a)
        txt.pack()
        check = tk.Checkbutton(master=frm_a)
        check.pack(fill=tk.X)
        radio = tk.Radiobutton(master=frm_a)
        radio.pack(fill=tk.Y)
        scale = tk.Scale(master=frm_a)
        scale.pack(fill=tk.BOTH)
        spin = tk.Spinbox(master=frm_a)
        spin.pack()
        btn_b = tk.Button()
        btn_b.place(x=20, y=10)
        frm_c = tk.Frame(width=10, height=10)
        frm_c.pack(fill=tk.BOTH)
        btn_c = tk.Button(master=frm_c, width=10, height=2)
        txt_b = tk.Text(master=frm_c, width=10, height=5)
        txt_c = tk.Text(master=frm_c, width=10, height=5)
        btn_d = tk.Button(master=frm_c, width=10, height=5)
        btn_c.grid(row=0, column=0, padx=1, pady=2, sticky="ne")
        txt_b.grid(row=0, column=1, padx=1, pady=2, sticky="ns")
        txt_c.grid(row=1, column=0, padx=1, pady=2, sticky="nsew")
        btn_d.grid(row=1, column=1, padx=1, pady=2)
        btn_d.bind("<Button-1>", new_click)
        frm_c.columnconfigure(0, weight=1, minsize=20)
        frm_c.columnconfigure(1, weight=1, minsize=20)
        frm_c.rowconfigure(0, weight=1, minsize=20)
        frm_c.rowconfigure(1, weight=1, minsize=20)'''
        frm_d = tk.Frame()
        frm_d.pack()
        InterfaceTkinter.canvas = tk.Canvas(master=frm_d)
        InterfaceTkinter.canvas.grid(row=0, column=0)
        oval = InterfaceTkinter.canvas.create_oval(0, 0, 100, 100)
        InterfaceTkinter.linha = InterfaceTkinter.canvas.create_line(50, 50, 50 + (50 * math.cos(math.radians(InterfaceTkinter.angulo))),
                                  50 - (50 * math.sin(math.radians(InterfaceTkinter.angulo))))
        # canvas.delete(line)
        print(math.cos(math.radians(0)))
        #InterfaceTkinter.canvas.bind('<Motion>', InterfaceTkinter.aumentar_angulo)
        InterfaceTkinter.canvas.bind('<Key>', InterfaceTkinter.aumentar_angulo)

        InterfaceTkinter.window.mainloop()  # Necessário para mostrar a janela

    @staticmethod
    def new_click(event):
        print("Algo")

    @staticmethod
    def aumentar_angulo(event):
        InterfaceTkinter.canvas.delete(InterfaceTkinter.linha)
        InterfaceTkinter.angulo += 1
        linha = InterfaceTkinter.canvas.create_line(50, 50, 50 + (50 * math.cos(math.radians(InterfaceTkinter.angulo))),
                                   50 - (50 * math.sin(math.radians(InterfaceTkinter.angulo))))


if __name__ == "__main__":
    InterfaceTkinter()