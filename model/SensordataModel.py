class SensordataModel:

    @staticmethod
    def status_open_closed(device, values):
        try:
            if not all(x is None for x in values.values()):
                return ''.join(['Closed' if int(values[device]['a']) < 10 else 'Open ({}cm)'.format(values[device]['a'])])
        except TypeError as e:
            print('Something went wrong with reading: {}'.format(values))
            print(e)
        return None
