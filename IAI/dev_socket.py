import socket
import threading
from time import sleep

from Console import LOG, LOGR
from SQLLDB import DB

pr = print
print = LOG


def noprnt():
    global pr, print
    print = pr


class Dev_socket:
    start_stop_test = False
    def __init__(self):
        self.sockets_opens = {}  # opens sockets dict(key-port)
        self.rec_threads = []  # receive threads list
        self.IP = DB.get_IP()
        self.rec_data_dict = {}
        pass

    def set_ip(self, ip):
        self.IP = ip
        DB.update_IP(ip)

    def open(self, dic, out):
        if out == 'R':
            port = dic['port_Rx']
        elif out == 'T':
            port = dic['port_Tx']
        else:
            return
        if port in self.sockets_opens:
            return self.sockets_opens[port]
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.bind(('', port))
            self.sockets_opens[port] = server_socket
            if 'ID_User_test' in dic.keys():
                print('Open port %s for test %s OK' % (port, dic['ID_User_test']))
            if 'Device' in dic.keys():
                print('Open port %s for dev %s OK' % (port, dic['Device']))
            return self.sockets_opens[port]
        except socket.error as er:
            print(port, er)
            return str(port) + ":" + str(er)

    def hex_to_byte(self, st):
        b = b''
        for n in range(0, len(st), 2):
            try:
                b += int(st[n: n + 2], 16).to_bytes(1, 'little')
            except:
                b += int('0', 16).to_bytes(1, 'little')
        return b

    def send_to(self, dic):
        port_from = dic['port_Tx']
        port_to = dic['port_Rx']
        message = dic['Data']
        if dic['Data_type'] == 'HEX':
            message = self.hex_to_byte(dic['Data'])

        if not port_from in self.sockets_opens:
            sock = self.open(dic, 'T')
            if not port_from in self.sockets_opens:
                return 'ERRor open socket %s:%s ' % (port_from, sock)
        try:
            if isinstance(message, bytes):
                b_message = len(message).to_bytes(2, 'little')
                b_message += int(0).to_bytes(2, 'little')
                b_message += message

            elif isinstance(message, str):
                b_message = len(message).to_bytes(2, 'little')
                b_message += int(0).to_bytes(2, 'little')
                b_message += message.encode()
            else:
                b_message = len(str(message)).to_bytes(2, 'little')
                b_message += int(0).to_bytes(2, 'little')
                b_message += str(message).encode()
            print('send(%s->%s): %s' % (port_from, port_to, b_message.hex()))
            self.sockets_opens[port_from].sendto(b_message, (self.IP, port_to))
            return b_message
        except socket.error as er:
            return 'Error %s send (%s:%s) ' % (er, self.IP, port_to)

    # Run receive thread
    def receive(self, dic):
        port = dic['port_Rx']
        if port not in self.sockets_opens:
            self.open(dic, 'R')
            if port not in self.sockets_opens:
                return 'can not open %s ' % (port,)
        thread = threading.Thread(target=self.thread_receive, args=(port,))
        thread.start()

    def thread_receive(self, port):
        if port in self.rec_threads:
            return
        self.rec_threads.append(port)
        print(' RUN receive thread %s OK' % port)
        n = 1
        while True:
            try:
                data, adr = self.sockets_opens[port].recvfrom(1024)
                print('received(%s<-%s):' % (port, adr[1]),data.hex())
                if port not in self.rec_data_dict.keys():
                    self.rec_data_dict[port] = []
                self.rec_data_dict[port].append(data[4:])
            except socket.error as er:
                print(f'closed port:{port}')
                self.rec_threads.remove(port)
                break
            except:
                print('closed', port)
                self.rec_threads.remove(port)
                break

    # {'ID_User_test': 257, 'Type_test': '444', 'ST_Test_Name': 'abc', 'Device_name_Tx': 'UART_4',
    #  'Device_name_Rx': 'UART_5', 'Date': '2021-11-29 09:51:58.630399', 'Packets_count': 1, 'Rate': 1, 'Data': 'ss',
    #  'port_Tx': 4444, 'port_Rx': 5555}

    def thread_run_test(self, dic_test):
        try:
            rate = float(dic_test['Rate'])
        except:
            print('error Rate')
            return
        try:
            count = int(dic_test['Packets_count'])
        except:
            print('error Count')
            return
        # =============================================
        type_test = dic_test['user_test_type']
        # ==========================================
        if dic_test['port_Rx'] in dev_socket.rec_data_dict:
            del (dev_socket.rec_data_dict[dic_test['port_Rx']])
        dd = b''
        for i in range(count):
            if not dev_socket.start_stop_test:
                LOGR('%s Stoped' % dic_test['ST_Test_Name'])
                print('%s Stoped' % dic_test['ID_User_test'])
                break
            dd = self.send_to(dic_test)
            sleep(rate)

        try:
            wiat_time = int(dic_test['WAIT'].get())
        except:
            dic_test['WAIT'].set(globals()['vDfWait'])
            wiat_time = int(dic_test['WAIT'].get())

        LOGR('[%s:%s] wait for answer time %s'% (dic_test['ID_User_test'], dic_test['ST_Test_Name'],wiat_time))
        n = 1
        while dic_test['port_Rx'] not in dev_socket.rec_data_dict:
            sleep(1)
            n += 1
            if n > wiat_time:
                LOGR('[%s:%s] test filed received 0' % (dic_test['ID_User_test'], dic_test['ST_Test_Name']))
                return
        n = 0

        if type_test == 'CMP' or 'HEX' in type_test  or 'ASCII' in type_test :
            if 'HEX' in type_test :
                cmp_text = self.hex_to_byte( dic_test['cmp_HEX'])
            elif 'ASCII' in type_test :
                cmp_text = dic_test['cmp_ASCII'].encode()
            else:
                cmp_text = dd[4:]
            sl = wiat_time
            while n != count:
                try:
                    dev_socket.rec_data_dict[dic_test['port_Rx']].remove(cmp_text)
                    n += 1
                except:
                    if sl:
                        sleep(1)
                        sl -= 1
                    else:
                        break

            LOGR('[%s:%s] sent %s rec %s result:%s' %
                 (dic_test['ID_User_test'], dic_test['ST_Test_Name'], count, n, ('FAILED', "PASS")[n == count]))
        else:
            n = 0
            c = 1
            while n < wiat_time:
                if len(dev_socket.rec_data_dict[dic_test['port_Rx']]) > 0:
                    text = dev_socket.rec_data_dict[dic_test['port_Rx']].pop(0)
                    try:
                        text = text.decode()
                    except:
                        text = str(text.hex())
                    LOGR('[%s:%s:%s] :%s' % (dic_test['ID_User_test'], dic_test['ST_Test_Name'], c, text))
                    n = 0
                    c += 1
                else:
                    sleep(1)
                    n += 1
        LOGR('%s ended' % dic_test['ST_Test_Name'])

        print('%s ended' % dic_test['ID_User_test'])
        pass

    def count(self):
        return len(self.sockets_opens)

    def rec_count(self):
        return len(self.rec_threads)

    def close(self, port):
        if port in self.sockets_opens:
            self.sockets_opens[port].close()
            del (self.sockets_opens[port])


# Global for all
dev_socket = Dev_socket()  # Class for socket todo from dev_socket.py

if __name__ == "__main__":
    pass
