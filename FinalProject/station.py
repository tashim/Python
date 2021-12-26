import datetime


class Station():

    """
    class Station -station data at time
    """
    def __init__(self,msg,from_string,sock=None,addr=None,thrd=None):
        """
        function __init__ inits station
        :param msg: message/file name with station data
        :param from_string: true if from string/false if from file
        """
        if from_string:
            x=msg.split(' ')
            self.station_id=int(x[0])
            self.date=None#x[1]+' '+x[2]
            self.alarm1=int(x[3])
            self.alarm2=int(x[4])
        else:
            file = open(msg, "r")
            self.station_id = int(file.readline())
            self.date = None#datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.alarm1 = int(file.readline())
            self.alarm2 = int(file.readline())
            file.close()
        self.addr=addr
        self.socket=sock
        self.thread=thrd

    def __repr__(self):
        """
        function __repr__ represents station
        """
        if self.date:
            dt=self.date
        else:
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.date=dt
        msg = "{0} {1} {2} {3}".format(self.station_id, dt, self.alarm1, self.alarm2)
        return msg