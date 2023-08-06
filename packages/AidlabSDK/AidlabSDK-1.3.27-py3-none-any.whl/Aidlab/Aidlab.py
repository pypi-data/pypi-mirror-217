#
# Aidlab.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabSDK import AidlabSDK
from Aidlab.AidlabPeripheral import AidlabPeripheral

class Aidlab:

    def __init__(self):
        # Container for AidlabSDK libs
        self.aidlab_sdk = {}
        self.aidlab_peripheral = AidlabPeripheral(self)

    def create_aidlabSDK(self, aidlab_address):
        self.aidlab_sdk[aidlab_address] = AidlabSDK(self, aidlab_address)
        self.aidlab_sdk[aidlab_address].setup_user_callback()
        self.aidlab_sdk[aidlab_address].setup_synchronization_callback()

    def destroy(self, aidlab_address):
        self.aidlab_sdk[aidlab_address].destroy()

    def connect(self, real_time_signal, sync_signal=[], aidlabsMAC=None):
        self.aidlab_peripheral.run(real_time_signal, sync_signal, aidlabsMAC)

    def disconnect(self, aidlab_address):
        self.aidlab_peripheral.disconnect(aidlab_address)
	
    def did_connect_aidlab(self, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_connect_aidlab()

    def did_disconnect_aidlab(self, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_disconnect_aidlab()

    def did_receive_raw_temperature(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_temperature(data)

    def did_receive_raw_ecg(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_ecg(data)

    def did_receive_raw_respiration(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_respiration(data)
    
    def did_receive_raw_battery_level(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_battery(data)

    def did_receive_raw_imu_values(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_motion(data)

    def did_receive_raw_orientation(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_orientation(data)
    
    def did_receive_raw_steps(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_steps(data)

    def did_receive_raw_activity(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_activity(data)
    
    def did_receive_raw_heart_rate(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_heart_rate(data)

    def did_receive_raw_health_thermometer(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_health_thermometer(data)

    def did_receive_raw_sound_volume(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].calculate_sound_volume(data)

    def did_receive_raw_cmd_value(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_receive_raw_cmd_value(data)

    def did_receive_raw_firmware_revision(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_receive_firmware_revision(data)

    def did_receive_raw_hardware_revision(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_receive_hardware_revision(data)

    def did_receive_raw_manufacture_name(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_receive_manufacture_name(data)

    def did_receive_raw_serial_number(self, data, aidlab_address):
        self.aidlab_sdk[aidlab_address].did_receive_serial_number(data)

    def get_command(self, aidlab_address, message):
        return self.aidlab_sdk[aidlab_address].get_command(message)

    def get_collect_command(self, aidlab_address, realTime, sync):
        return self.aidlab_sdk[aidlab_address].get_collect_command(realTime, sync)

    def start_synchronization(self, address):
        self.aidlab_peripheral.start_synchronization(address)        

    def stop_synchronization(self, address):
        self.aidlab_peripheral.stop_synchronization(address)
    
    def send(self, address, command):
        self.aidlab_peripheral.send(address, command)

    # -- Aidlab callbacks ----------------------------------------------------------------------------

    def did_connect(self, aidlab):
        pass

    def did_disconnect(self, aidlab):
        pass

    def did_receive_ecg(self, aidlab, timestamp, values):
        """Called when a new ECG samples was received.
        """
        pass

    def did_receive_respiration(self, aidlab, timestamp, values):
        """Called when a new respiration samples was received.
        """
        pass

    def did_receive_respiration_rate(self, aidlab, timestamp, value):
        """Called when a new respiration sample was received.
        """
        pass

    def did_receive_battery_level(self, aidlab, state_of_charge):
        """If battery monitoring is enabled, this event will notify about Aidlab's
           state of charge. You never want Aidlab to run low on battery, as it can
           lead to it's sudden turn off. Use this event to inform your users about
           Aidlab's low energy.
        """
        pass

    def did_receive_skin_temperature(self, aidlab, timestamp, value):
        """Called when a skin temperature was received.
        """
        pass

    def did_receive_accelerometer(self, aidlab, timestamp, ax, ay, az):
        """Called when new accelerometer data were received.
        """
        pass

    def did_receive_gyroscope(self, aidlab, timestamp, gx, gy, gz):
        """Called when new gyroscope data were received.
        """
        pass

    def did_receive_magnetometer(self, aidlab, timestamp, mx, my, mz):
        """Called when new magnetometer data were received.
        """
        pass

    def did_receive_orientation(self, aidlab, timestamp, roll, pitch, yaw):
        """Called when received orientation, represented in RPY angles.
        """
        pass

    def did_receive_body_position(self, aidlab, timestamp, body_position):
        """Called when received body position.
        """
        pass

    def did_receive_quaternion(self, aidlab, timestamp, qw, qx, qy, qz):
        """Called when new quaternion data were received.
        """
        pass

    def did_receive_activity(self, aidlab, timestamp, activity):
        """Called when activity data were received.
        """
        pass

    def did_receive_steps(self, aidlab, timestamp, steps):
        """Called when total steps did change.
        """
        pass

    def did_receive_heart_rate(self, aidlab, timestamp, heart_rate):
        """Called when a heart rate did change.
        """
        pass

    def did_receive_rr(self, aidlab, timestamp, rr):
        pass

    def wear_state_did_change(self, aidlab, state):
        """Called when a significant change of wear state did occur. You can use
           that information to make decisions when to start processing data, or
           display short user guide on how to wear Aidlab in your app.
        """
        pass

    def did_receive_pressure(self, aidlab, timestamp, values):
        pass

    def pressure_wear_state_did_change(self, aidlab, wear_state):
        pass

    def did_receive_sound_volume(self, aidlab, timestamp, sound_volume):
        pass

    def did_receive_signal_quality(self, aidlab, timestamp, value):
        pass

    def did_detect_exercise(self, aidlab, exercise):
        pass

    def did_receive_command(self, aidlab):
        pass

    def did_detect_user_event(self, aidlab, timestamp):
        pass

    # -- Aidlab Synchronization ---------------------------------------------------------------------

    def sync_state_did_change(self, aidlab, sync_state):
        pass

    def did_receive_unsynchronized_size(self, aidlab, unsynchronized_size, sync_bytes_per_second):
        pass

    def did_receive_past_ecg(self, aidlab, timestamp, values):
        pass

    def did_receive_past_respiration(self, aidlab, timestamp, values):
        pass

    def did_receive_past_respiration_rate(self, aidlab, timestamp, value):
        pass

    def did_receive_past_skin_temperature(self, aidlab, timestamp, value):
        pass

    def did_receive_past_accelerometer(self, aidlab, timestamp, ax, ay, az):
        pass

    def did_receive_past_gyroscope(self, aidlab, timestamp, gx, gy, gz):
        pass

    def did_receive_past_magnetometer(self, aidlab, timestamp, mx, my, mz):
        pass

    def did_receive_past_orientation(self, aidlab, timestamp, roll, pitch, yaw):
        pass

    def did_receive_past_body_position(self, aidlab, timestamp, body_position):
        pass

    def did_receive_past_quaternion(self, aidlab, timestamp, qw, qx, qy, qz):
        pass

    def did_receive_past_activity(self, aidlab, timestamp, activity):
        pass

    def did_receive_past_steps(self, aidlab, timestamp, steps):
        pass

    def did_receive_past_heart_rate(self, aidlab, timestamp, heart_rate):
        pass

    def did_receive_past_rr(self, aidlab, timestamp, rr):
        pass

    def did_receive_past_pressure(self, aidlab, timestamp, values):
        pass

    def did_receive_past_sound_volume(self, aidlab, timestamp, sound_volume):
        pass

    def did_receive_past_user_event(self, aidlab, timestamp):
        pass

    def did_receive_past_signal_quality(self, aidlab, timestamp, value):
        pass


