import binascii
import socket
import _thread

from django.core.serializers import json

from .models import TrackerPosition
from .Tracker import Tracker
from .TrackerAlivePacket import TrackerAlivePacket
from .TrackerLogin import TrackerLogin
from .utils.crc import crc16


class GT06Information(object):
    _HOST = '0.0.0.0'  # Server IP
    _PORT = 55000  # Server Port
    _BUFFER = 1024  # Connection Buffer

    # status
    _location = '12'
    _status = '13'
    _string = '15'
    _alarm = '16'
    _query = '1A'
    _command = '80'
    _login = '01'
    
    # socket    
    _tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _tcp_extra = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def listner(self):

        self._tcp.bind((self._HOST, self._PORT))
        self._tcp.listen(1)

        while True:
            con, client = self._tcp.accept()
            _thread.start_new_thread(self._connected, tuple([con, client]))

        self._tcp.close()

    def _connected(self, con, client):
        print('connection by: {0}'.format(client))

        self._valid_operations(con, client)

        print('end connection \n')
        con.close()
        _thread.exit()

    def _valid_operations(self, con, client):

        global tracker
        tracker = None

        while True:

            msg = con.recv(self._BUFFER)

            if not msg:
                break

            else:
                msg = binascii.hexlify(bytearray(msg)).decode('utf-8')

                if not self._valid_package(msg[-4:-8], msg):
                    continue

            protocol = msg[6:8]

            if tracker is not None:

                if protocol == self._location:
                    if not self._save_location(tracker, msg):
                        break

                elif protocol == self._status:
                    if not self._receive_heartbeat(tracker, msg, con):
                        break

                elif protocol == self._string:
                    print('String information')

                elif protocol == self._alarm:
                    self._receive_alarm(tracker, msg)

                elif protocol == self._query:
                    print('GPS, query address information by phone number')

                elif protocol == self._command:
                    print('Command information sent by the server to the terminal')

            elif protocol == self._login:
                tracker = self._validate_login_data(msg, con)
                if tracker is None:
                    break

    @staticmethod
    def _valid_package(error_check, msg):

        error_check = error_check.replace(' ', '')
        msg = msg.replace(' ', '')

        if crc16(binascii.unhexlify(msg[4:-8])) == error_check:
            print('---- Package validate error ----')
            return False

        return True

    @staticmethod
    def _validate_login_data(msg, con):
        print('---- Login message ----')

        serial = int(''.join([str(int(x, 16)) for x in msg[8:24]]))
        serial_number = int(msg[24:28], 16)
        tracker = Tracker.objects.filter(imei=serial).first()

        if tracker is not None:

            return_msg = '78 78 05 01 00 01 {serial_number}'.format(serial_number=format(serial_number+1, '04x')).replace(' ', '')
            return_msg += '{error_crc} 0D 0A'.format(error_crc=crc16(binascii.unhexlify(return_msg[4:]))).replace(' ', '')
            return_msg_binary = binascii.unhexlify(return_msg.upper())

            con.send(return_msg_binary)
            TrackerLogin.objects.create(tracker=tracker, message=msg, return_message=return_msg)

            print('valid login')
            return tracker

        else:
            print('login not valid')
            return None

    def _save_location(self, tracker, msg):
        print('---- Location message ----')

        datetime = self._extract_datetim(msg[8:20])

        satellites = int(msg[20:22], 16)

        latitude = int(msg[22:30], 16)
        latitude = latitude/30000
        latitude_int = int(latitude/60)
        latitude = '{0}.{1}'.format(latitude_int, str((latitude - latitude_int*60)).replace('.', ''))

        longitude = int(msg[22:30], 16)
        longitude = longitude / 30000
        longitude_int = int(longitude / 60)
        longitude = '{0}.{1}'.format(longitude_int, str(longitude - (longitude_int * 60)).replace('.', ''))

        speed = int(msg[38:40], 16)

        course = self._terminal_course(msg[40:44])
        direction_longitude = course['direction_longitude']
        direction_latitude = course['direction_latitude']
        direction_angle = course['direction_angle']

        mmc = int(msg[44:48], 16)
        mnc = int(msg[48:50], 16)
        lac = int(msg[50:54], 16)

        cell_id = int(msg[54:60], 16)
        serial_number = int(msg[60:64], 16)

        TrackerPosition.objects.create(tracker=tracker, latitude=latitude, longitude=longitude, gps_datetime=datetime,
                                       speed=speed, message=msg, direction_longitude=direction_longitude,
                                       direction_latitude=direction_latitude, direction_angle=direction_angle,)

        print('position saved')
        return True

    def _receive_heartbeat(self, tracker, msg, con):
        print('---- Heartbeat message ----')

        terminal_information = self._terminal_information(msg[8:10])

        terminal_information['voltage'] = int(16.6666 * int(msg[10:12], 16))
        terminal_information['signal'] = int(20 * int(msg[12:14], 16))
        terminal_information['language'] = 'chinese' if msg[16:18] == '01'  else 'english'

        alarm = msg[14:16]
        terminal_information['alarm'] = True

        if alarm == '00':
            terminal_information['has_alarm'] = False
            terminal_information['alarm_status'] = 'normal'

        elif alarm == '01':
            terminal_information['alarm_status'] = 'sos'

        elif alarm == '02':
            terminal_information['alarm'] = 'power_cut_alarm'

        elif alarm == '03':
            terminal_information['alarm'] = 'shock_alarm'

        elif alarm == '04':
            terminal_information['alarm'] = 'fence_in_alarm'

        elif alarm == '05':
            terminal_information['alarm'] = 'fence_out_alarm'

        terminal_information = json.dumps(terminal_information)

        serial_number = int(msg[18:22], 16)

        return_msg = '78 78 05 13 {serial_number}'.format(serial_number=format(serial_number + 1, '04x')).replace(' ', '')
        return_msg += '{error_crc} 0D 0A'.format(error_crc=crc16(binascii.unhexlify(return_msg[4:]))).replace(' ', '')
        return_msg = binascii.unhexlify(return_msg.upper())

        con.send(return_msg)

        TrackerAlivePacket.objects.create(tracker=tracker, terminal_information=terminal_information, message=msg,
                                          return_message=return_msg)

        return True

    @staticmethod
    def _alarm_receive(tracker, msg):
        print('---- Alarm message ----')
        # view 5.3 -> 16
        pass


    @staticmethod
    def _terminal_information(terminal_information):
        result = {}

        # To binary string
        binary = bin(int(terminal_information, 16))[2:]

        # Bit 7
        result['gas_oil_electricity_connected'] = True if binary[7] == '1' else False
        # Bit 6
        result['gps_tracking_on'] = True if binary[6] == '1' else False
        # Bit 3~5
        result['sos'] = True if binary[3:6] == '100' else False
        result['low_battery'] = True if binary[3:6] == '011' else False
        result['power_cut'] = True if binary[3:6] == '010' else False
        result['shock_alarm '] = True if binary[3:6] == '001' else False
        result['normal'] = True if binary[3:6] == '000' else False
        # Bit 2
        result['change_on'] = True if binary[2] == '1' else False
        # Bit 1
        result['acc_high'] = True if binary[1] == '1' else False
        # Bit 0
        result['activated'] = True if binary[0] == '1' else False

        return result

    @staticmethod
    def _terminal_course(course):
        result = {}

        # To binary string
        binary = bin(int(course, 16))[2:]

        # Bit 13 (or bit 5 in byte 2)
        result['gps_real_time'] = True if binary[3] == '0' else False
        # Bit 12 (or bit 4 in byte 2)
        result['gps_positioned'] = True if binary[4] == '0' else False
        # Bit 11 (or bit 3 in byte 2)
        result['direction_longitude'] = 'east' if binary[5] == '0' else 'weast'
        # Bit 10 (or bit 2 in byte 2)
        result['direction_latitude'] = 'south' if binary[6] == '0' else 'north'
        # Bit 0~9 (or bit 1 in byte 1 to bit 2 in byte 2)
        result['direction_angle'] = int(course[7:], 2)

        return result

    @staticmethod
    def _extract_datetim(datetime):

        datetime = '20' + ''.join([str(int(datetime[i:i + 2], 16)).zfill(2) for i in range(0, len(datetime), 2)])
        datetime = '{}{}{}{}/{}{}/{}{} {}{}:{}{}:{}{}'.format(*datetime)

        return datetime
