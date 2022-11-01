import random
from random import choice, randint, shuffle
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import uuid
import res

PERIOD = res.periods1
# множитель
NUM = 0  # формируется cbox-ами str(тариф) + str(период) т.е. 1 + 11 = 111
FACTOR = res.factor  # множитель кол-ва символов в файле берется из res файла
COLOR = "#F5F5DC"


def n(): return str(randint(1111, 999999))


def uid_rnum():

    """ Generate request code from uuid node.
    The mask is: n1 - uid3 - uid1 - n2 - uid2 - n3 """

    # Get uid num string
    uid = str(uuid.getnode())
    # Reverse uid
    num = uid[::-1]
    # Make control_nums from uid
    x1 = num[:4]
    x2 = num[4:9]
    x3 = num[9:]
    # Redy request code / rnum
    rnum = f"{n()}-{x3}-{x1}-{n()}-{x2}-{n()}"
    # result
    return rnum


def rnum_uid(rnum: str):

    """ Get uid node from rnum """

    l = rnum.split('-')
    mask = f"{l[2]}{l[4]}{l[1]}"
    uid = mask[::-1]
    
    return uid


def gui():

    """ Интерфейс программы / GUI """

    def update_button():

        """ Функционал кнопки Update / 'Update' button actions """

        num = entry_rnum.get()
        uid = rnum_uid(rnum=num)
        label_uid.config(text=uid)

    def generate_button():

        """ Функционал кнопки генерации файла лицензии / 'Generate' button actions """

        global NUM, FACTOR

        uid = label_uid.cget('text')  # 246321139097169
        uid1 = uid[1:3]  # START CONTROL NUMBER
        uid2 = uid[6:8]  # END CONTROL NUMBER

        if NUM != 0:

            number = int(NUM) * FACTOR
            letters = [choice(res.letters) for _ in range(randint(number, number))]
            numbers = [choice(res.numbers) for _ in range(randint(number, number))]
            symbols = [choice(res.symbols) for _ in range(randint(number, number))]
            psw = letters + numbers + symbols
            shuffle(psw)
            psw.insert(10, f"{NUM}|")  # запись контрольного номера в файл после 10го символа + | после контр.символа (for inspecting in file)
            psw.insert(random.randint(20, 500), '|')
            psw.insert(random.randint(600, 1200), '|')
            psw.insert(random.randint(1300, 2000), '|')
            psw.pop(0)
            psw.pop(0)
            psw.insert(0, uid1)
            psw.pop(-1)
            psw.pop(-1)
            psw.append(uid2)
            data = ''.join(psw)

            with open('res.dat', 'w') as file:
                file.write(data)

            messagebox.showinfo(title="res.dat", message='res.dat file created successful!')

        else:
            messagebox.showerror(title="Error!", message="Please, select tarif and period!")

    #########################################################################################
    # GUI / Интерфейс программы -------------------------------------------------------------
    #########################################################################################

    rnum = uid_rnum()
    uid = rnum_uid(rnum=rnum)
    # Main window
    root = Tk()
    root.title("Gen")
    root.config(padx=5, pady=5)
    root.maxsize(width=350, height=250)
    # Label
    label_uid = Label(text=uid, width=40)
    label_uid.grid(column=0, row=0, columnspan=2)
    # Request code entry field
    entry_rnum = Entry(width=41, relief="sunken")
    entry_rnum.insert(0, uid_rnum())
    entry_rnum.config(state='normal', bg=COLOR)
    entry_rnum.grid(column=0, row=1, padx=3, pady=3, columnspan=2)
    # Label
    label = Label(text="Tarif / Period", width=12)
    label.grid(column=0, row=2, columnspan=2)
    # 
    def tarif_selected(event):

        """ Функция выбора тарифа для tarif_cbox / 'Pick Tarif' actions """

        global PERIOD
        if tarif_cbox.current() == 0:
            period_cbox['values'] = res.periods1
        elif tarif_cbox.current() == 1:
            period_cbox['values'] = res.periods2
        elif tarif_cbox.current() == 2:
            period_cbox['values'] = res.periods3

    # GUI селектор выбора тарифа / 'Tarif' selector
    n = StringVar()
    tarif_cbox = ttk.Combobox(root, width=17, textvariable=n, state="readonly")
    tarif_cbox['values'] = res.tarif
    tarif_cbox.bind("<<ComboboxSelected>>", tarif_selected)
    tarif_cbox.grid(column=0, row=3, pady=3, padx=3, sticky=NW)

    def period_selected(event):

        """ Функция выбора тарифа для period_cbox / 'Pick Period' actions """

        global NUM
        tarif_num = str(tarif_cbox.current() + 1)
        period_num = str(period_cbox.current() + 1)
        lic_number = tarif_num + period_num
        NUM = lic_number

    # GUI селектор выбора периода / 'Pick period' selector
    n2 = StringVar()
    period_cbox = ttk.Combobox(root, width=17, textvariable=n2, state="readonly")
    period_cbox.bind("<<ComboboxSelected>>", period_selected)
    period_cbox.grid(column=1, row=3, padx=3, pady=3, sticky=NW)
    # Кнопка Update / 'Update' button
    button_update = Button(text="Update", width=8, height=1, command=update_button)
    button_update.grid(column=1, row=5, padx=3, pady=3, sticky=SW)
    # Кнопка Generate / 'Generate' button
    start_button = Button(text="Generate", width=9, height=1, command=generate_button)
    start_button.grid(column=1, row=5, padx=3, pady=3, sticky=SE)

    root.mainloop()


gui()
