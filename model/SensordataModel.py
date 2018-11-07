class SensordataModel:

    @staticmethod
    def status_open_closed(device, values):
        return ''.join(['Closed' if int(values[device]['a']) < 10 else 'Open ({}cm)'.format(values[device]['a'])])
