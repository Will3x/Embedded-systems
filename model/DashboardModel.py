class DashboardModel:

    @classmethod
    def setup(cls):
        """ Called once from Main. """
        cls.mv_instances = {1: None, 2: None, 3: None, 4: None, 5: None}
        cls.prev_devices = cls.mv_instances.copy()

    @classmethod
    def get_mv_dict(cls, index=None):
        """ Returns dict of all MainView instances if the index parameter is None. If [index] is set,
        get MainView instance at given index. Acts as a getter for current MainView instances. """
        if index is not None:
            return cls.mv_instances.get(index)
        return cls.mv_instances

    @classmethod
    def add_mv(cls, index, mv_instance):
        """ Adds MainView object to mv_instances dictionary at position [index]. Returns True if successful. """
        cls.mv_instances[index] = mv_instance
        return cls.mv_instances[index] is mv_instance

    @classmethod
    def remove_mv(cls, index):
        """ Removes MainView object of mv_instances dictionary at position [index]. Will be replaced with: None.
        Returns True if successful. """
        cls.mv_instances[index] = None
        return cls.mv_instances[index] is None

    @classmethod
    def mv_empty(cls, index=None):
        """ Checks if there are no MainView objects in mv_instances. If [index] is set, only checks at given index.
        Returns True if empty, False if not. """
        if index is None:
            return all(cls.mv_instances.values()) is None
        return cls.mv_instances[index] is None

    @classmethod
    def set_prev_devices(cls, devices):
        """ Reassign prev_devices with [devices]. Returns if successful. """
        cls.prev_devices = devices.copy()
        return cls.prev_devices is devices.copy()

    @classmethod
    def prev_devices_empty(cls, index=None):
        """ Checks if there are no Devices in prev_devices. If [index] is set, only checks at given index.
        Returns True if empty, False if not. """
        if index is None:
            return all(device is None for device in cls.prev_devices.values())
        return cls.prev_devices[index] is None

    @classmethod
    def update_instances(cls, devices):
        """ Removes MainView object at specific index from mv_instances if devices[index] is also empty but
        prev_devices[index] and mv_instances[index] are not. """
        for index in devices.keys():
            if devices[index] is None and not cls.prev_devices_empty(index) and not cls.mv_empty(index):
                cls.get_mv_dict(index).close()
                cls.remove_mv(index)

    @staticmethod
    def get_status(index, values):
        """ Returns 'Open' or 'Closed' based on distance sensor data. """
        try:
            if not all(x == () for x in values.values()):
                return ''.join(['Closed' if int(values[index]['a']) < 10 else 'Open {}cm'.format(values[index]['a'])])
        except TypeError as e:
            print('DashboardModel.get_status: Something went wrong with reading: {}'.format(values))
        return None
