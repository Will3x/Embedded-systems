class SensordataModel:

    @staticmethod
    def status_open_closed(device, values):
        if not all(x == () for x in values.values()):
            return ''.join(['Closed' if int(values[device]['a']) < 10 else 'Open ({}cm)'.format(values[device]['a'])])
        return None
