import logging
from time import time

from pymavlink.dialects.v20.ardupilotmega import MAVLink_message

from .message_models import (
    Attitude,
    GlobalPositionInt,
    GPSRawInt,
    GPSStatus,
    Heartbeat,
    RadioStatus,
    RcChannelsRaw,
    ServoOutputRaw,
    SysStatus,
)

logger = logging.getLogger()


class UAVData:
    def __init__(self) -> None:
        self.heartbeat = Heartbeat()
        self.global_position_int = GlobalPositionInt()
        self.attitude = Attitude()
        self.gps_raw_int = GPSRawInt()
        self.gps_status = GPSStatus()
        self.radio_status = RadioStatus()
        self.rc_channel_raw = RcChannelsRaw()
        self.servo_output_raw = ServoOutputRaw()
        self.sys_status = SysStatus()

    def process_heartbeat(self, msg: MAVLink_message) -> None:
        self.heartbeat = Heartbeat.parse_obj(msg.to_dict())
        self.heartbeat.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.heartbeat.mavpackettype)

    def process_global_position_int(self, msg: MAVLink_message) -> None:
        self.global_position_int = GlobalPositionInt.parse_obj(msg.to_dict())
        self.global_position_int.timestamp_ms = int(time() * 1000)
        logger.debug(
            "received message type: %s", self.global_position_int.mavpackettype
        )

    def process_attitude(self, msg: MAVLink_message) -> None:
        self.attitude = Attitude.parse_obj(msg.to_dict())
        self.attitude.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.attitude.mavpackettype)

    def process_gps_raw_int(self, msg: MAVLink_message) -> None:
        self.gps_raw_int = GPSRawInt.parse_obj(msg.to_dict())
        self.gps_raw_int.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.gps_raw_int.mavpackettype)

    def process_gps_status(self, msg: MAVLink_message) -> None:
        self.gps_status = GPSStatus.parse_obj(msg.to_dict())
        self.gps_status.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.gps_status.mavpackettype)

    def process_radio_status(self, msg: MAVLink_message) -> None:
        self.radio_status = RadioStatus.parse_obj(msg.to_dict())
        self.radio_status.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.radio_status.mavpackettype)

    def process_rc_channels_raw(self, msg: MAVLink_message) -> None:
        self.rc_channel_raw = RcChannelsRaw.parse_obj(msg.to_dict())
        self.rc_channel_raw.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.rc_channel_raw.mavpackettype)

    def process_servo_output_raw(self, msg: MAVLink_message) -> None:
        self.servo_output_raw = ServoOutputRaw.parse_obj(msg.to_dict())
        self.servo_output_raw.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.servo_output_raw.mavpackettype)

    def process_sys_status(self, msg: MAVLink_message) -> None:
        self.sys_status = SysStatus.parse_obj(msg.to_dict())
        self.sys_status.timestamp_ms = int(time() * 1000)
        logger.debug("received message type: %s", self.sys_status.mavpackettype)
