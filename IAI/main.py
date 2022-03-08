import threading
from subprocess import Popen, PIPE
from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Combobox

from Console import *
from SQLLDB import *
from dev_socket import *

vDfWait = 3
vLoop = 1


def dic_split(d, i1, i2):
    li = list(d.items())
    li.insert(i2, li.pop(i1))
    d = dict(li)
    return d


def onFrameConfigure(canvas):
    # Reset the scroll region to encompass the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))


def is_int(inStr,c):
    if inStr == '': return True
    return inStr.isdigit()


def is_float(inStr):
    if inStr == '': return True
    try:
        r = float(inStr)
        return True
    except:
        return False


class Tests_for_run:

    def __init__(self, app):
        self.tests_list = {}
        self.top = LabelFrame(app, text='User TESTS for run')
        self.top.pack(fill='x')
        self.vIP = StringVar()
        self.vIP.trace_add("write", self.vIP_callback)
        app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.vDfWait = StringVar()
        self.vDfWait.trace_add("write", self.vDfWait_callback)
        self.vLoop = StringVar()
        self.vLoop.trace_add("write", self.vLoop_callback)
        self.vLoop.set(globals()['vLoop'])

        wt = DB.get_dfWait()
        if wt:
            self.vDfWait.set(wt)
            globals()['vDfWait'] = wt
        else:
            self.vDfWait.set(DB.get_dfWait())
            globals()['vDfWait'] = DB.get_dfWait()

        f_top = Frame(self.top)
        f_top.pack(fill=X, expand=False, padx=3, pady=3)

        c = Canvas(self.top, )
        self.frame_canvas = Frame(c)
        xscr = Scrollbar(self.top, orient=HORIZONTAL, command=c.xview)
        c.config(xscrollcommand=xscr.set)
        xscr.pack(side="bottom", fill="x")
        yscr = Scrollbar(self.top, orient="vertical", command=c.yview)
        c.config(yscrollcommand=yscr.set)
        yscr.pack(side="right", fill="y")
        c.pack(fill="both", expand=True)
        c.create_window((4, 4), window=self.frame_canvas, anchor="nw")
        self.frame_canvas.bind("<Configure>", lambda event, c=c: onFrameConfigure(c))

        f_med = Frame(app)
        f_med.pack(fill=X, expand=False, padx=3, pady=3)
        paddings = {'padx': 20, 'pady': 1}
        self.eIp = Entry(f_med, textvariable=self.vIP, font=('Digital-7', 14), width=15)
        self.eIp.pack(side=LEFT, **paddings)
        self.vIP.set(dev_socket.IP)

        Button(f_med, text='PING', command=self.ping).pack(side=LEFT, **paddings)
        Button(f_top, text='Load', command=lambda: Load_User_Test(self)).pack(side=LEFT, **paddings)
        Button(f_top, text='Clear', command=self.clean_dic).pack(side=LEFT, **paddings)
        Button(f_med, text='PORTS SETUP', command=lambda: Devices()).pack(side=LEFT, **paddings)
        Button(f_med, text='LISTEN Port', command=lambda: Start_Port_to_Receive()).pack(side=LEFT, **paddings)
        Button(f_med, text='STOP Test', command=self.all_tests_stop).pack(fill=X, side=LEFT, **paddings)
        Button(f_med, text='RUN Test Thread', command=self.all_tests_start).pack(fill=X, side=LEFT, **paddings)
        Button(f_med, text='RUN Test ', command=lambda: threading.Thread(target=self.all_tests_run).start()).pack(
            fill=X, side=LEFT, **paddings)
        Label(f_top, text="df wait Time").pack(side=LEFT, )
        Entry(f_top, textvariable=self.vDfWait, width=3).pack(fill=X, **paddings, side=LEFT, )
        Label(f_top, text="LOOP").pack(side=LEFT, )
        Entry(f_top, textvariable=self.vLoop, width=3).pack(fill=X, **paddings, side=LEFT, )

        Button(f_top, text='Save Load LIST', command=lambda: Save_List_Test(self)).pack(side=RIGHT, **paddings)

        self.show_list()
        # ================================================================================

    @staticmethod
    def check(ip):
        if re.search('^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)', ip):
            for t in ip.split('.'):
                if int(t) > 255:
                    return False
            return True
        return False

    def vIP_callback(self, *args):
        ip = self.vIP.get().replace(' ', '')
        if self.check(ip):
            self.vIP.set(ip)
            self.eIp['foreground'] = 'black'
            dev_socket.set_ip(ip)
        else:
            self.eIp['foreground'] = 'red'

    def vDfWait_callback(self, *args):
        wait = self.vDfWait.get().replace(' ', '')
        if wait.isdigit():
            self.vDfWait.set(wait)
            globals()['vDfWait'] = wait
            DB.update_dfWait(wait)

    def vLoop_callback(self, *args):
        wait = self.vLoop.get().replace(' ', '')
        if wait.isdigit():
            self.vLoop.set(wait)
            globals()['vLoop'] = wait
            # DB.update_dfWait(wait)

    def ping(self):
        print('run ping...' + "ping  " + self.vIP.get())
        proc = Popen("ping  " + self.vIP.get(), stdout=PIPE)
        b = 1
        while b:
            try:
                b = proc.stdout.read(1)
                LOGR(b.decode(), end='c')
            except:
                LOGR(b, end='c')
            app.update()

    def show_list(self):
        self.clean()
        paddings = {'padx': 1, 'ipadx': 1, 'pady': 2, 'ipady': 1, 'sticky': NSEW}
        # Names columns of Table in Frame "Status"
        names = "ID_User_test,Type_test," \
                "ST_Test_Name,Device_name_Tx,Device_name_Rx,Packets_count,Rate," \
                "Data_type,Data,user_test_type,cmp_with,WAIT"
        Label(self.frame_canvas, text=str('N%'), borderwidth="1", relief="solid").grid(row=0, column=0, **paddings)
        col = 1
        for lc_in in names.split(','):
            if lc_in == 'Packets_count':
                name_lc = Label(self.frame_canvas, text='Count', borderwidth="1", relief="solid")
                name_lc.grid(row=0, column=col, **paddings)
            else:
                name_lc = Label(self.frame_canvas, text=lc_in, borderwidth="1", relief="solid")
                name_lc.grid(row=0, column=col, **paddings)
            col += 1
        Label(self.frame_canvas, text=str('Show'), borderwidth="1", relief="solid").grid(row=0, column=col, **paddings)
        n = 1
        for key in self.tests_list:
            col = 1
            Label(self.frame_canvas, text=str(n), borderwidth="1", relief="solid").grid(row=n, column=0, **paddings)
            for lc_in in names.split(','):

                if lc_in == 'WAIT':
                    # self.tests_list[key]['WAIT'] = StringVar()
                    en_c_2 = Entry(self.frame_canvas, width=5, validate="key",
                                   textvariable=self.tests_list[key]['WAIT'])
                    en_c_2['validatecommand'] = (en_c_2.register(is_int), '%P', '%s')
                    en_c_2.grid(row=n, column=col, **paddings)
                elif lc_in == 'cmp_with':
                    if 'ASCII' in self.tests_list[key]['user_test_type']:
                        Label(self.frame_canvas, text=str(self.tests_list[key]['cmp_ASCII']),
                              borderwidth="1", relief="solid") \
                            .grid(row=n, column=col, **paddings)
                    elif 'HEX' in self.tests_list[key]['user_test_type']:
                        Label(self.frame_canvas, text=str(self.tests_list[key]['cmp_HEX']),
                              borderwidth="1", relief="solid") \
                            .grid(row=n, column=col, **paddings)
                    elif 'NO' in self.tests_list[key]['user_test_type'].upper():
                        Label(self.frame_canvas, text='', borderwidth="1", relief="solid") \
                            .grid(row=n, column=col, **paddings)
                    else:
                        Label(self.frame_canvas, text=str(self.tests_list[key]['Data']),
                              borderwidth="1", relief="solid") \
                            .grid(row=n, column=col, **paddings)
                else:
                    Label(self.frame_canvas, text=self.tests_list[key][lc_in], borderwidth="1", relief="solid"). \
                        grid(row=n, column=col, **paddings)
                col += 1
            vCheckbutton = BooleanVar()
            chb = Checkbutton(self.frame_canvas, variable=vCheckbutton, )
            chb['command'] = lambda d=self.tests_list[key], c=vCheckbutton: self.isChecked(d, c)
            chb.grid(row=n, column=col, )
            vCheckbutton.set(self.tests_list[key]['show'])

            Button(self.frame_canvas, text='Remove', command=lambda data=key: self.rem(data)) \
                .grid(row=n, column=col + 2, **paddings)
            Button(self.frame_canvas, text='edit', command=lambda d=self.tests_list[key]: self.edit_test(d)) \
                .grid(row=n, column=col + 1, **paddings)
            Button(self.frame_canvas, text='UP', command=lambda d=n: self.up(d)) \
                .grid(row=n, column=col + 3, **paddings)
            Button(self.frame_canvas, text='DWN', command=lambda d=n: self.down(d)) \
                .grid(row=n, column=col + 4, **paddings)
            n += 1
        Label(self.frame_canvas, text='', borderwidth="1").grid(row=n + 2, column=0, **paddings)

    def up(self, n):
        n = n - 1
        if n <= 0:
            return
        self.tests_list = dic_split(self.tests_list, n, n - 1)
        self.show_list()

    def down(self, n):
        if n >= len(self.tests_list):
            return
        n = n - 1
        self.tests_list = dic_split(self.tests_list, n, n + 1)
        self.show_list()

    def isChecked(self, d, chb):
        d['show'] = chb.get()

    def rem(self, d):
        del (self.tests_list[d])
        self.show_list()

    def edit_test(self, d):
        edit_Test_wind(d, self)
        self.show_list()

    def add_test(self, dic):
        self.tests_list[dic['ID_User_test']] = dic
        self.show_list()

    def clean_dic(self):
        self.tests_list= {}
        for child in self.frame_canvas.winfo_children():
            child.destroy()

    def clean(self):
        for child in self.frame_canvas.winfo_children():
            child.destroy()


    def all_tests_start(self):
        dev_socket.start_stop_test = True
        for key in self.tests_list:
            ret = dev_socket.receive(self.tests_list[key])
            # TODO run thread for send
            threading.Thread(target=dev_socket.thread_run_test, args=(self.tests_list[key],)).start()

    def all_tests_run(self):
        n = 1
        dev_socket.start_stop_test = True
        for key in self.tests_list:
            dev_socket.receive(self.tests_list[key])
            # TODO run  send
        try:
            if int(self.vLoop.get()) < 1:
                self.vLoop.set(1)
        except:
            self.vLoop.set(1)

        while n <= int(self.vLoop.get()):
            print('run loop N%', n, )
            for key in self.tests_list:
                if dev_socket.start_stop_test:
                    dev_socket.thread_run_test(self.tests_list[key], )
                else:
                    print('Test aborted')
                    return
            n += 1

    def all_tests_stop(self):
        dev_socket.start_stop_test = False

    def on_closing(self):
        global pr, print
        print = pr
        noprnt()
        li = list(dev_socket.sockets_opens.keys())
        for port in li:
            dev_socket.close(port)
        app.destroy()


class Save_List_Test:
    def __init__(self, master):
        self.master = master
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Load User tests')
        frame_medium = Frame(self.top)  # !!!!!!!!!!!!!!!!!!!!!!!!
        frame_medium.pack(fill="both", expand=True, ipady=1)

        canvas_port = Canvas(frame_medium, )

        scroll_port = Scrollbar(frame_medium, orient="vertical", command=canvas_port.yview)
        canvas_port.config(yscrollcommand=scroll_port.set)

        scroll_port.pack(side="right", fill="y")
        canvas_port.pack(fill="both", expand=True)

        self.fr_col_1 = Frame(canvas_port)
        canvas_port.create_window((4, 4), window=self.fr_col_1, anchor="nw")
        self.fr_col_1.bind("<Configure>", lambda event, canvas_port=canvas_port: onFrameConfigure(canvas_port))

        self.varData = StringVar()
        self.varLog = StringVar()
        Entry(self.top, width=15, textvariable=self.varData).pack()
        Button(self.top, text='Save LIST', command=self.save).pack()
        # Button(self.top, text='Save LIST', command=self.load).pack()
        Label(self.top, text='', textvariable=self.varLog).pack()
        self.load()

    def clean(self):
        for child in self.fr_col_1.winfo_children():
            child.destroy()

    def save(self):
        name = self.varData.get().replace(':', '').replace(',', '').replace(' ', '')
        if name == "":
            self.varLog.set('Name error')
            return
        if len(self.master.tests_list) <= 0:
            self.varLog.set('List of tests is empty')
            return
        d = ""
        for key in self.master.tests_list:
            t = self.master.tests_list[key]
            d += f"%s:%s:%s," % (t['ID_User_test'], t['show'], t['WAIT'].get())
        DB.save_list_tests(name, d)
        self.load()

    def load(self):
        self.clean()
        paddings = {'padx': 1, 'ipadx': 1, 'pady': 2, 'ipady': 1, 'sticky': EW}
        opt = {'relief': "solid"}

        i = 0
        Label(self.fr_col_1, text=' Name ', **opt).grid(row=i, column=0, **paddings)
        Label(self.fr_col_1, text=' Count tests ', **opt).grid(row=i, column=1, **paddings)
        i = i + 1
        for r in DB.load_list_tests():
            di = {}
            for d in r[1].replace(" ", "").split(","):
                if (d == ""):
                    continue
                t = d.split(':')
                di[t[0]] = (t[1], t[2])

            Label(self.fr_col_1, text=str(r[0]), **opt).grid(row=i, column=0, **paddings)
            Label(self.fr_col_1, text=str(len(di.keys())), **opt).grid(row=i, column=1, **paddings)
            Button(self.fr_col_1, text='upload',
                   command=lambda c=di: self.upload(c)).grid(row=i, column=2)
            Button(self.fr_col_1, text='del',
                   command=lambda c=r[0]: self.delete(c)).grid(row=i, column=3)

            i += 1
        pass

    def upload(self, d):
        print(d)
        rez = DB.usertest_load(tuple(d.keys()))
        drez = {}
        for dic in rez:
            dic["WAIT"] = StringVar()
            dic["WAIT"].set(d[str(dic['ID_User_test'])][1])
            dic["show"] = d[str(dic['ID_User_test'])][0]
            drez[str(dic['ID_User_test'])] = dic
        self.master.tests_list = drez

        # print(rez)
        self.master.show_list()

    def delete(self, d):
        DB.del_list_tests(d)
        self.load()


class Load_User_Test:

    def __init__(self, master):
        self.master = master
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Load User tests')
        w = app.winfo_screenwidth()
        h = app.winfo_screenheight()
        self.top.geometry('{}x{}'.format(int(w / 10 * 9), int(h / 10 * 4)))

        f_list = Frame(self.top)
        canv_load = Canvas(f_list)
        self.fr_c_l = Frame(canv_load)
        f_button = Frame(self.top)

        self.fr_c_l.bind("<Configure>", lambda event, canv_load=canv_load: onFrameConfigure(canv_load))

        scr_load = Scrollbar(canv_load, orient=HORIZONTAL, command=canv_load.xview)
        scr_load.pack(side="bottom", fill="both")
        canv_load.config(xscrollcommand=scr_load.set)
        scr_load = Scrollbar(canv_load, orient=VERTICAL, command=canv_load.yview)
        scr_load.pack(side="right", fill="both")

        canv_load.create_window((4, 4), window=self.fr_c_l, anchor="nw")
        canv_load.config(yscrollcommand=scr_load.set)

        canv_load.pack(fill="both", expand=True, )
        f_list.pack(fill="both", expand=True, )
        f_button.pack(fill="both", expand=False)
        # self.fr_c_l=canv_load
        ##############################################
        self.get_from_db()

        Button(f_button, text='New Test', command=self.new_test). \
            pack(side='left', padx=5)
        Button(f_button, text="STANDART TEST  SETUP", command=lambda: St_test_setup(self)). \
            pack(side='left', padx=5, )
        Button(f_button, text="Type TEST  SETUP", command=lambda: New_Type_test_setup(self)). \
            pack(side='left', padx=5)

    def clean(self):
        for child in self.fr_c_l.winfo_children():
            child.destroy()

    def new_test(self):
        New_Test_wind(self)

    def get_from_db(self):
        self.clean()
        paddings = {'padx': 1, 'ipadx': 1, 'pady': 2, 'ipady': 1, 'sticky': EW}
        opt = {'relief': "solid"}
        # from DB load all
        list_ut = DB.integration_load()
        num = 0
        names = "ID_User_test,Type_test,ST_Test_Name,Device_name_Tx,Device_name_Rx," \
                "Packets_count,Rate,Data_type,Data,user_test_type,cmp_with"
        Label(self.fr_c_l, text='', ).grid(row=100, column=1, **paddings)
        for cn in names.split(','):
            Label(self.fr_c_l, text=cn, **opt).grid(row=0, column=num, **paddings)
            num += 1
        if len(list_ut) > 0:
            row = 1
            for dic in list_ut:
                num = 0
                for key in names.split(','):
                    if key == 'cmp_with':
                        if 'ASCII' in dic['user_test_type']:
                            Label(self.fr_c_l, text=str(dic['cmp_ASCII']), **opt).grid(row=row, column=num, **paddings)
                        elif 'HEX' in dic['user_test_type']:
                            Label(self.fr_c_l, text=str(dic['cmp_HEX']), **opt).grid(row=row, column=num, **paddings)
                        elif 'NO' in dic['user_test_type'].upper():
                            Label(self.fr_c_l, text='', **opt).grid(row=row, column=num, **paddings)
                        else:
                            Label(self.fr_c_l, text=str(dic['Data']), **opt).grid(row=row, column=num, **paddings)
                    else:
                        Label(self.fr_c_l, text=str(dic[key]), **opt).grid(row=row, column=num, **paddings)
                    num += 1

                Button(self.fr_c_l, text='Add Test',
                       command=lambda d=dic:
                       self.add_load(d)).grid(row=row, column=21, )
                Button(self.fr_c_l, text='Delete Test',
                       command=lambda d=dic['ID_User_test']:
                       self.delete_userTest(d)).grid(row=row, column=22, )
                row += 1
        Label(self.fr_c_l, text='', ).grid(row=100, column=0, )

    def add_load(self, d):
        d['show'] = True
        d['WAIT'] = StringVar()
        d['WAIT'].set(globals()['vDfWait'])
        self.master.add_test(d)

    def delete_userTest(self, d):
        DB.delete(d)
        self.get_from_db()


class New_Test_wind:
    def __init__(self, master=None):
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Create new User test')

        self.parent = master
        self.data_backup = ['', '']
        self.utest = {}
        self.utest['cmp_ASCII'] = ''
        self.utest['cmp_HEX'] = ''

        Label(self.top, text='Type of test').grid(row=0, column=0, padx=5)
        Label(self.top, text='Test name').grid(row=0, column=1, padx=5)
        Label(self.top, text='Num of packets').grid(row=0, column=2, padx=5)
        Label(self.top, text='Sending_Rate').grid(row=0, column=3, padx=5)

        self.opt_type = Combobox(self.top, state="readonly", value=DB.test_type_list())
        self.opt_type.bind('<<ComboboxSelected>>', self.cbx2)
        self.opt_type.grid(row=1, column=0, padx=5)

        self.cb_stTestName = Combobox(self.top, state="readonly", value=[])  # Combobox "Test name"
        self.cb_stTestName.grid(row=1, column=1, padx=5)

        # creating field "Num of packets" in Frame "New Test"
        self.en_c_1 = Entry(self.top, width=15, validate="key")
        self.en_c_1['validatecommand'] = (self.en_c_1.register(is_int), '%P')
        self.en_c_1.grid(row=1, column=2, padx=5)

        # creating field "Sending_Rate" in Frame "New Test"
        self.en_c_2 = Entry(self.top, width=15, validate="key")
        self.en_c_2['validatecommand'] = (self.en_c_2.register(is_float), '%P')
        self.en_c_2.grid(row=1, column=3, padx=5)

        """
            send data
        """
        self.cb_data_t = Combobox(self.top, state="readonly", value=('ASCII', 'HEX'))
        self.cb_data_t.bind('<<ComboboxSelected>>', self.cb_ascii_change)
        self.cb_data_t.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

        self.varData = StringVar()
        self.varData.trace_add("write", lambda a, b, c: self.var_changed(self.cb_data_t, self.varData))
        Entry(self.top, width=15, textvariable=self.varData) \
            .grid(row=3, column=1, padx=5, columnspan=10, sticky=EW)

        """
            comper data
        """
        self.cb_cmp_t = Combobox(self.top, state="readonly", value=('No cmp', 'CMP', 'CMP_ASCII', 'CMP_HEX'))
        self.cb_cmp_t.bind('<<ComboboxSelected>>', lambda cc=self.cb_cmp_t: self.cb_cmp_change(self.cb_cmp_t))
        self.cb_cmp_t.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

        self.vcbCMP_data = StringVar()
        self.vcbCMP_data.trace_add("write", lambda a, b, c: self.var_changed(self.cb_cmp_t, self.vcbCMP_data))
        self.en_CmpData = Entry(self.top, width=15, textvariable=self.vcbCMP_data)
        self.en_CmpData.grid(row=4, column=1, padx=5, columnspan=10, sticky=EW)

        Button(self.top, text='Save test', command=self.confirmation).grid(row=5, column=0, pady=15)

        self.cb_data_t.current(1)
        self.cb_ascii_change()
        self.cb_cmp_t.current(0)
        self.cb_cmp_change(self.cb_cmp_t)

    def cb_cmp_change(self, cb):
        if 'ASCII' in cb.get():
            self.vcbCMP_data.set(self.utest['cmp_ASCII'])
            self.en_CmpData.grid(row=4, column=1, padx=5, columnspan=10, sticky=EW)
            self.var_changed(cb, self.vcbCMP_data)
        elif 'HEX' in cb.get():
            self.vcbCMP_data.set(self.utest['cmp_HEX'])
            self.en_CmpData.grid(row=4, column=1, padx=5, columnspan=10, sticky=EW)
            self.var_changed(cb, self.vcbCMP_data)

        else:
            self.en_CmpData.grid_remove()

    def var_changed(self, cb, var: StringVar):
        if 'HEX' not in cb.get():
            self.utest['cmp_ASCII'] = self.vcbCMP_data.get()
            return True
        text = ''
        for t in var.get():
            if not t in '0123456789abcdefABCDEF':
                continue
            else:
                text += t
        var.set(text)
        self.utest['cmp_HEX'] = self.vcbCMP_data.get()

    def cb_ascii_change(self, *args):
        if self.cb_data_t.get() == 'ASCII':
            self.data_backup[1] = self.varData.get()
            self.varData.set(self.data_backup[0])
        else:
            self.data_backup[0] = self.varData.get()
            self.varData.set(self.data_backup[1])

    def cbx2(self, *args):
        var_type = self.opt_type.get()
        if var_type == '':
            self.cb_stTestName["value"] = []
        else:
            self.cb_stTestName["value"] = DB.tests_names_by_type(var_type)
            if len(self.cb_stTestName["value"]) > 0:
                self.cb_stTestName.current(0)

    def confirmation(self):

        name = 'StTest, Packets_count, Rate, Data,Data_type, Date,user_test_type,cmp_ASCII,cmp_HEX'

        if self.cb_stTestName.get() != '':
            self.utest['StTest'] = self.cb_stTestName.get()
        else:
            print('Error ', "Input Test_Name error ")
            return
        try:
            self.utest['Packets_count'] = int(self.en_c_1.get())
        except:
            self.utest['Packets_count'] = 1
        try:
            self.utest['Rate'] = float(self.en_c_2.get())
        except:
            self.utest['Rate'] = 0.1

        self.utest['Data'] = self.varData.get()
        self.utest['Data_type'] = self.cb_data_t.get()
        self.utest['user_test_type'] = self.cb_cmp_t.get()
        self.utest['Date'] = datetime.datetime.now().strftime('%d-%m-%y')
        DB.save_user_test(self.utest)
        if self.parent:
            self.parent.get_from_db()
        self.top.destroy()


class edit_Test_wind:
    def __init__(self, dic, parent):
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Edit  User test')
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.dic = dic
        self.parent = parent
        self.data_backup = ['', '']

        Label(self.top, text='Type of test').grid(row=0, column=0, padx=5)
        Label(self.top, text='Test name').grid(row=0, column=1, padx=5)
        Label(self.top, text='Num of packets').grid(row=0, column=2, padx=5)
        Label(self.top, text='Sending_Rate').grid(row=0, column=3, padx=5)
        Label(self.top, text=self.dic['Type_test']).grid(row=1, column=0, padx=5)
        Label(self.top, text=self.dic['ST_Test_Name']).grid(row=1, column=1, padx=5)

        # creating field "Num of packets" in Frame "New Test"
        self.var_pack_count = StringVar()
        self.var_pack_count.trace_add("write",
                                      lambda a, b, c: self.varRATE_COUNT_changed('Packets_count', self.var_pack_count))
        self.var_pack_count.set(dic['Packets_count'])
        ent = Entry(self.top, width=15, validate="key", textvariable=self.var_pack_count)
        ent['validatecommand'] = (ent.register(is_int), '%P')
        ent.grid(row=1, column=2, padx=5)

        # creating field "Sending_Rate" in Frame "New Test"
        self.var_rate = StringVar()
        self.var_rate.trace_add("write", lambda a, b, c: self.varRATE_COUNT_changed("Rate", self.var_rate))
        self.var_rate.set(dic['Rate'])
        self.en_Rate = Entry(self.top, width=15, validate="all", textvariable=self.var_rate, )
        self.en_Rate['validatecommand'] = (self.en_Rate.register(is_float), '%P')
        self.en_Rate.grid(row=1, column=3, padx=5)

        """
            send data
        """
        self.cb_data_t = Combobox(self.top, state="readonly", value=('ASCII', 'HEX'))
        self.cb_data_t.bind('<<ComboboxSelected>>', self.cb_ascii_change)
        self.cb_data_t.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

        self.varData = StringVar()
        self.varData.trace_add("write", lambda a, b, c: self.var_changed(self.cb_data_t, self.varData))
        Entry(self.top, width=15, textvariable=self.varData) \
            .grid(row=3, column=1, padx=5, columnspan=10, sticky=EW)

        """
            comper data
        """
        self.cb_cmp_t = Combobox(self.top, state="readonly", value=('No cmp', 'CMP', 'CMP_ASCII', 'CMP_HEX'))
        self.cb_cmp_t.bind('<<ComboboxSelected>>', lambda cc=self.cb_cmp_t: self.cb_cmp_change(self.cb_cmp_t))
        self.cb_cmp_t.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

        self.vcbCMP_data = StringVar()
        self.vcbCMP_data.trace_add("write", lambda a, b, c: self.var_cmp_changed(self.cb_cmp_t, self.vcbCMP_data))
        self.en_CmpData = Entry(self.top, width=15, textvariable=self.vcbCMP_data)
        self.en_CmpData.grid(row=4, column=1, padx=5, columnspan=10, sticky=EW)

        Button(self.top, text='Save test', command=self.confirmation). \
            grid(row=6, column=1, padx=5, pady=5, )

        if self.dic['Data_type'] in self.cb_data_t['value']:
            self.cb_data_t.set(self.dic['Data_type'])
        else:
            self.cb_data_t.current(0)
        self.varData.set(self.dic['Data'])
        if self.dic['user_test_type'] == None:
            self.cb_cmp_t.current(0)
            self.dic['user_test_type'] = self.cb_cmp_t.get()
        else:
            self.cb_cmp_t.set(str(self.dic['user_test_type']))
        self.cb_cmp_change(self.cb_cmp_t)
        self.parent.show_list()

    def var_changed(self, cb, var: StringVar):
        if 'HEX' in cb.get():
            text = ''
            for t in var.get():
                if not t in '0123456789abcdefABCDEF':
                    continue
                else:
                    text += t
            var.set(text)

        self.dic['Data'] = var.get()
        self.dic['Data_type'] = cb.get()
        self.parent.show_list()

    def var_cmp_changed(self, cb, var: StringVar):
        if 'HEX' in cb.get():
            text = ''
            for t in var.get():
                if not t in '0123456789abcdefABCDEF':
                    continue
                else:
                    text += t
            var.set(text)
            self.dic['cmp_HEX'] = text
        else:
            self.dic['cmp_ASCII'] = var.get()
        self.parent.show_list()

    def cb_cmp_change(self, cb):
        if 'ASCII' in cb.get() or 'HEX' in cb.get():
            self.en_CmpData.grid(row=4, column=1, padx=5, columnspan=10, sticky=EW)
            if 'HEX' in cb.get():
                self.vcbCMP_data.set(self.dic['cmp_HEX'])
            else:
                self.vcbCMP_data.set(self.dic['cmp_ASCII'])
            self.var_cmp_changed(cb, self.vcbCMP_data)
        else:
            self.en_CmpData.grid_remove()
        self.dic['user_test_type'] = cb.get()
        self.parent.show_list()

    def cb_ascii_change(self, *args):
        if self.cb_data_t.get() == 'ASCII':
            self.data_backup[1] = self.varData.get()
            self.varData.set(self.data_backup[0])
        else:
            self.data_backup[0] = self.varData.get()
            self.varData.set(self.data_backup[1])
        self.parent.show_list()

    def varRATE_COUNT_changed(self, key, var):
        if var.get() == '':
            return
        if 'Rate' in key:
            self.dic[key] = float(var.get())
        else:
            self.dic[key] = int(var.get())
        self.parent.show_list()

    def on_closing(self):
        # self.parent.show_list()
        self.top.destroy()

    def update_test(self):
        self.parent.show_list()

    def confirmation(self):
        if self.dic['Packets_count'] == '':
            self.dic['Packets_count'] = 1
        if self.dic['Rate'] == '':
            self.dic['Rate'] = 0.1
        DB.update_user_test(self.dic)
        self.parent.show_list()
        self.top.destroy()


class Start_Port_to_Receive:
    def __init__(self):
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Start_Port_to_Receve')

        # self.top.geometry('300x150+300+300')
        self.dev = DB.ports_by_dev()
        self.run_count = 100
        self.vcount = StringVar()
        self.vcount.set("Threads %s is run" % dev_socket.rec_count())
        Label(self.top, textvariable=self.vcount).pack(padx=10, pady=10)
        self.thr = Combobox(self.top, state="readonly")
        self.thr.pack(padx=10, pady=10)

        Button(self.top, text='Stop thread', command=self.rm_thread) \
            .pack(padx=10, pady=10)

        Label(self.top, text="Devices for listening").pack(padx=10, pady=10)
        self.device = Combobox(self.top, state="readonly")
        self.device.pack(padx=10, pady=10)
        Button(self.top, text='Start', command=self.start_receive) \
            .pack(padx=10, pady=10)
        self.top.after(1, self.loop)

    def update_combo(self):
        notrun = []
        isrun = []
        threads = dev_socket.rec_threads
        for key in self.dev.keys():
            if self.dev[key][1] in threads:
                isrun.append(key)
            else:
                notrun.append(key)
        self.device['value'] = notrun
        if not self.device.get() in notrun:
            if len(notrun):
                self.device.current(0)
            else:
                self.device.set('')
        self.thr['value'] = isrun
        if not self.thr.get() in isrun:
            if len(isrun):
                self.thr.current(0)
            else:
                self.thr.set('')
        self.vcount.set("Threads %s is run" % dev_socket.rec_count())
        self.run_count = dev_socket.rec_count()

    def loop(self):
        if self.run_count != len(dev_socket.rec_threads):
            self.update_combo()
        self.top.after(100, self.loop)

    def rm_thread(self):
        if self.thr.get() == '': return
        dev_socket.close(self.dev[self.thr.get()][1])

    def start_receive(self):
        if self.device.get() != '':
            dev = DB.ports_by_dev(self.device.get())
            if self.device.get() in dev:
                dic = {}
                dic['port_Tx'] = dev[self.device.get()][0]
                dic['port_Rx'] = dev[self.device.get()][1]
                dic['Device'] = self.device.get()
                dev_socket.receive(dic)


class New_Type_test_setup:
    def __init__(self, parent=None):
        self.parent = parent
        top = Toplevel()
        top.grab_set()
        top.title('TYPE test setup')
        top.geometry('500x300')

        canv_load = Canvas(top)
        self.frame = Frame(canv_load)
        self.frame.bind("<Configure>", lambda event, canv_load=canv_load: onFrameConfigure(canv_load))

        scr_load = Scrollbar(canv_load, orient=VERTICAL, command=canv_load.yview)

        canv_load.create_window((4, 4), window=self.frame, anchor="nw")
        canv_load.config(yscrollcommand=scr_load.set)
        canv_load.pack(fill=BOTH, expand=True)
        scr_load.pack(side="right", fill="y")

        frame_in = Frame(top)
        frame_in.pack()
        Label(frame_in, text='Type of test').pack(side=LEFT)

        self.opt_type = StringVar()
        entry_new_type = Entry(frame_in, textvariable=self.opt_type)
        entry_new_type.pack(side=LEFT)

        Button(top, text="Save Type Test",
               command=self.save_new_type).pack()
        self.load_list()

    def save_new_type(self):
        if self.opt_type.get() == '':
            print("showinfo", 'Type of test is empty. Choice any type!')
            return None
        else:
            DB.save_new_type(self.opt_type.get())
        self.load_list()

    def load_list(self):
        for child in self.frame.winfo_children():
            child.destroy()

        type_list = DB.test_type_list()
        n = 0
        for tl in type_list:
            var = StringVar()
            var.set(tl)
            Entry(self.frame, text=tl, textvariable=var).grid(row=n, column=0, ipadx=1)
            Button(self.frame, text='rename'
                   , command=lambda a=tl, b=var: self.rename(a, b)).grid(row=n, column=1, padx=5)
            Button(self.frame, text='delete'
                   , command=lambda a=tl: self.delete(a)
                   ).grid(row=n, column=2, padx=5)
            n += 1

    def rename(self, old: str, new: StringVar):
        DB.update_test_type(old, new.get())
        if self.parent:
            self.parent.get_from_db()

    def delete(self, old: str):
        DB.delete_test_type(old)
        self.load_list()
        if self.parent:
            self.parent.get_from_db()
        rm = []
        for t in run_list_top.tests_list:
            if run_list_top.tests_list[t]['Type_test'] == old:
                rm.append(t)
        for t in rm:
            del run_list_top.tests_list[t]
        run_list_top.show_list()


class St_test_setup():
    def __init__(self, parent=None):
        self.parent = parent
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Standard test setup')
        dev_names = list(DB.ports_by_dev().keys())

        frame_medium = Frame(self.top)  # !!!!!!!!!!!!!!!!!!!!!!!!
        frame_medium.pack(fill="both", expand=True, ipady=1)

        canvas_port = Canvas(frame_medium, )

        scroll_port = Scrollbar(frame_medium, orient="vertical", command=canvas_port.yview)
        canvas_port.config(yscrollcommand=scroll_port.set)

        scroll_port.pack(side="right", fill="y")
        canvas_port.pack(fill="both", expand=True)

        self.fr_col_1 = Frame(canvas_port)
        canvas_port.create_window((4, 4), window=self.fr_col_1, anchor="nw")
        self.fr_col_1.bind("<Configure>", lambda event, canvas_port=canvas_port: onFrameConfigure(canvas_port))

        #

        fr_col_1 = Frame(self.top)  # !!!!!!!!!!!!!!!!!!!!!!!!
        fr_col_1.pack()

        Label(fr_col_1, text='Type of test').grid(row=0, column=0, padx=5)
        Label(fr_col_1, text='Test name').grid(row=0, column=1, padx=5)
        Label(fr_col_1, text='Device_name_TX').grid(row=0, column=2, padx=5)
        Label(fr_col_1, text='Device_name_RX').grid(row=0, column=3, padx=5)

        self.opt_type = Combobox(fr_col_1, state="readonly", value=DB.test_type_list())
        self.opt_type.grid(row=1, column=0, padx=5)

        self.t_n = Entry(fr_col_1, width=30)
        self.t_n.grid(row=1, column=1, padx=5)
        self.dev_name_Tx = Combobox(fr_col_1, state="readonly", value=dev_names)
        self.dev_name_Tx.grid(row=1, column=2, padx=5)

        self.dev_name_Rx = Combobox(fr_col_1, state="readonly", value=dev_names)
        self.dev_name_Rx.grid(row=1, column=3, padx=5)

        Button(fr_col_1, text="Save New ST Test", command=self.save_st_test).grid(row=2, column=0, pady=5)
        self.Log = StringVar()
        Label(fr_col_1, text='Type of test', textvariable=self.Log).grid(row=1000, columnspan=10, column=0, padx=5)
        self.load_table()

    def load_table(self):
        frame = self.fr_col_1
        for child in frame.winfo_children():
            child.destroy()

        opt = {'relief': "solid"}
        paddings = {'padx': 1, 'ipadx': 1, 'pady': 2, 'ipady': 1, 'sticky': NSEW}

        li = DB.St_Test_List()
        Label(frame, text='Type of test', **opt).grid(row=0, column=0, **paddings)
        Label(frame, text='Test name', **opt).grid(row=0, column=1, **paddings)
        Label(frame, text='Device_name_TX', **opt).grid(row=0, column=2, **paddings)
        Label(frame, text='Device_name_RX', **opt).grid(row=0, column=3, **paddings)

        row = 2
        for st in li:
            Label(frame, text=st[0], **opt).grid(row=row, column=0, **paddings)
            Label(frame, text=st[1], **opt).grid(row=row, column=1, **paddings)
            Label(frame, text=st[2], **opt).grid(row=row, column=2, **paddings)
            Label(frame, text=st[3], **opt).grid(row=row, column=3, **paddings)
            Button(frame, text='Delete', **opt, command=lambda keyx=st[1]: self.rem(keyx)) \
                .grid(row=row, column=4, **paddings)
            row += 1
        Label(frame, text='', ).grid(row=row, column=3, **paddings)

    def rem(self, key):
        DB.delete_ST_test(key)
        self.load_table()
        rm = []
        if self.parent:
            self.parent.get_from_db()
        for t in run_list_top.tests_list:
            if run_list_top.tests_list[t]['ST_Test_Name'] == key:
                rm.append(t)
        for t in rm:
            del run_list_top.tests_list[t]
        run_list_top.show_list()

    def save_st_test(self):
        self.Log.set('')
        if self.t_n.get() == '':
            self.Log.set('showinfo: Test name is empty. Enter any name of test!')
            return None
        dev_name_Tx = self.dev_name_Tx.get()
        if dev_name_Tx == '':
            self.Log.set('showinfo: Name of Device_Tx is empty. Choice any Name!')
            return None
        dev_name_Rx = self.dev_name_Rx.get()
        if dev_name_Rx == '':
            self.Log.set('showinfo: Name of Device_Rx is empty. Choice any Name!')
            return None
        if self.t_n.get() == '':
            self.Log.set('showinfo: Test name is empty. Enter any name of test!')
            return None
        ret = DB.save_stand_test(self.opt_type.get(), self.t_n.get(), dev_name_Tx, dev_name_Rx)
        if ret != None:
            self.Log.set(ret)
        self.load_table()

    def load_from_db(self):
        for child in self.fr_col_1.winfo_children():
            child.destroy()

        devises = DB.ports_by_dev()
        self.n_tx = {}
        self.n_rx = {}
        n = 1
        for key in devises:
            Label(self.fr_col_1, text=key).grid(row=n, column=0, sticky=NSEW, padx=5)

            v = StringVar()
            Entry(self.fr_col_1, width=10, textvariable=v).grid(row=n, column=1, sticky=NSEW, padx=5)
            self.n_tx[key] = v

            v = StringVar()
            Entry(self.fr_col_1, width=10, textvariable=v).grid(row=n, column=2, sticky=NSEW, padx=5)
            self.n_rx[key] = v
            Button(self.fr_col_1, text='Delete', command=lambda keyx=key: self.rem(keyx)) \
                .grid(row=n, column=3)
            n += 1
        n = 99


class Devices():
    def __init__(self):

        self.top = Toplevel()
        self.top.grab_set()
        self.top.title('Devices')

        frame_medium = Frame(self.top)  # !!!!!!!!!!!!!!!!!!!!!!!!
        frame_medium.pack(fill="both", expand=True, ipady=1)

        canvas_port = Canvas(frame_medium, )

        scroll_port = Scrollbar(frame_medium, orient="vertical", command=canvas_port.yview)
        canvas_port.config(yscrollcommand=scroll_port.set)

        scroll_port.pack(side="right", fill="y")
        canvas_port.pack(fill="both", expand=True)

        self.fr_col_1 = Frame(canvas_port)
        canvas_port.create_window((4, 4), window=self.fr_col_1, anchor="nw")
        self.fr_col_1.bind("<Configure>", lambda event, canvas_port=canvas_port: onFrameConfigure(canvas_port))

        #
        Label(self.fr_col_1, text='Device').grid(row=0, column=0, sticky=NSEW)
        Label(self.fr_col_1, text='Port TX').grid(row=0, column=1, sticky=NSEW)
        Label(self.fr_col_1, text='Port Rx').grid(row=0, column=2, sticky=NSEW)

        fr_col_1 = Frame(self.top)  # !!!!!!!!!!!!!!!!!!!!!!!!
        fr_col_1.pack()

        self.new_name = StringVar()
        self.log = StringVar()
        self.new_pt = StringVar()
        self.new_pr = StringVar()
        self.new_name.set('new')
        self.new_pt.set('new')
        self.new_pr.set('new')

        Label(fr_col_1, text='', textvariable=self.log).pack()
        Entry(fr_col_1, width=10, textvariable=self.new_name).pack(side=LEFT, )
        Entry(fr_col_1, width=10, textvariable=self.new_pt).pack(side=LEFT, )
        Entry(fr_col_1, width=10, textvariable=self.new_pr).pack(side=LEFT, )
        Button(fr_col_1, text='add', command=self.add).pack(side=LEFT, )

        Button(self.top, text='SAVE', command=self.update_ports).pack()

        self.update_table()

    def load_from_db(self):
        for child in self.fr_col_1.winfo_children():
            child.destroy()

        devises = DB.ports_by_dev()
        self.n_tx = {}
        self.n_rx = {}
        n = 1
        for key in devises:
            Label(self.fr_col_1, text=key).grid(row=n, column=0, sticky=NSEW, padx=5)

            v = StringVar()
            Entry(self.fr_col_1, width=10, textvariable=v).grid(row=n, column=1, sticky=NSEW, padx=5)
            self.n_tx[key] = v

            v = StringVar()
            Entry(self.fr_col_1, width=10, textvariable=v).grid(row=n, column=2, sticky=NSEW, padx=5)
            self.n_rx[key] = v
            Button(self.fr_col_1, text='Delete', command=lambda keyx=key: self.rem(keyx)) \
                .grid(row=n, column=3)
            n += 1
        n = 99

    def add(self):
        devises = DB.ports_by_dev()
        err = ''
        if self.new_name.get() == '':
            err = 'name ? '

        if self.new_name.get() in devises.keys():
            err += 'name exist '
        try:
            int(self.new_pr.get())
            int(self.new_pt.get())
        except:
            err += 'port ? '
        if err == '':
            DB.input_dev((self.new_name.get(), self.new_pt.get(), self.new_pr.get()))
            self.update_table()
        else:
            self.log.set(err)

    def rem(self, key):
        DB.del_ports(key)
        self.update_table()

    def update_ports(self):
        update_d = []
        for key in self.n_tx.keys():
            update_d.append((self.n_tx[key].get(), self.n_rx[key].get(), key))
        DB.save_ports(update_d)
        self.update_table()

    def update_table(self):
        self.load_from_db()
        devises = DB.ports_by_dev()
        for key in self.n_tx.keys():
            self.n_tx[key].set(devises[key][0])
            self.n_rx[key].set(devises[key][1])


if __name__ == "__main__":
    app = Tk()
    w = app.winfo_screenwidth()
    h = app.winfo_screenheight()
    app.geometry('{}x{}'.format(int(w / 10 * 9), int(h / 10 * 8)))
    # app.option_add('*Font', 'Helvetica 11')
    app.option_add('*Font', 'Digital-7 13')
    app.title('IAI_MAIN')

    style = Style()
    style.configure('TButton', font=('Helvetica', 10, 'italic'), borderwidth='4', )
    style.map('TButton', foreground=[('active', '!disabled', 'blue')], background=[('active', 'red')], )

    run_list_top = Tests_for_run(app)
    Concole(app)

    menubar = Menu(app)
    filemenu = Menu(menubar, tearoff=0, )
    filemenu.add_command(label="Port Setup", command=Devices)
    filemenu.add_command(label="Type test Setup", command=New_Type_test_setup)
    filemenu.add_command(label="Standrd test Setup", command=St_test_setup)
    filemenu.add_command(label="New test Setup", command=New_Test_wind)
    filemenu.add_command(label="Listen Ports", command=Start_Port_to_Receive)
    filemenu.add_command(label="Load TESTS", command=lambda: Load_User_Test(run_list_top))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=app.quit)

    menubar.add_cascade(label="SETUP", menu=filemenu)
    app.config(menu=menubar)
    pr = print
    print = LOG

    app.mainloop()
