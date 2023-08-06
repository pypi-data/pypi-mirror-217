##########################################################################
# Copyright (c) 2010-2022 Robert Bosch GmbH
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
##########################################################################

"""
Can Communication Channel using PCAN hardware
*********************************************

:module: cc_pcan_can

:synopsis: CChannel implementation for CAN(fd) using PCAN API from python-can

.. currentmodule:: cc_pcan_can

"""

import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

try:
    import can
    import can.bus
    import can.interfaces.pcan.basic as PCANBasic
except ImportError as e:
    raise ImportError(
        f"{e.name} dependency missing, consider installing pykiso with 'pip install pykiso[can]'"
    )


from pykiso import CChannel, Message

MessageType = Union[Message, bytes]

log = logging.getLogger(__name__)


class PcanFilter(logging.Filter):
    """Filter specific pcan logging messages"""

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if the specified record is to be logged. It will not if
        it is a pcan bus error message

        :param record: record of the event to filter if it is a pcan bus error

        :return: True if the record should be logged, or False otherwise.
        """
        return not record.getMessage().startswith("Bus error: an error counter")


class CCPCanCan(CChannel):
    """CAN FD channel-adapter."""

    def __init__(
        self,
        interface: str = "pcan",
        channel: str = "PCAN_USBBUS1",
        state: str = "ACTIVE",
        trace_path: str = "",
        trace_size: int = 10,
        bitrate: int = 500000,
        is_fd: bool = True,
        enable_brs: bool = False,
        f_clock_mhz: int = 80,
        nom_brp: int = 2,
        nom_tseg1: int = 63,
        nom_tseg2: int = 16,
        nom_sjw: int = 16,
        data_brp: int = 4,
        data_tseg1: int = 7,
        data_tseg2: int = 2,
        data_sjw: int = 2,
        is_extended_id: bool = False,
        remote_id: int = None,
        can_filters: list = None,
        logging_activated: bool = True,
        bus_error_warning_filter: bool = False,
        **kwargs,
    ):
        """Initialize can channel settings.

        :param interface: python-can interface modules used
        :param channel: the can interface name
        :param state: BusState of the channel
        :param trace_path: path to write the trace (can be a folder or a .trc file)
        .. note:: If the .trc file already exists, it will be overwritten. If the trace_path
          is an existing folder, a default name will be generated for the trace file
          containing the timestamp. If the trace_path is a non-existent folder, the
          folder will be created and the default name will be used for the trace
          file. If the trace_path is not defined by the user, the default file will be
          saved in the current working directory.
        :param trace_size: maximum size of the trace (in MB)
        :param bitrate: Bitrate of channel in bit/s,ignored if using CanFD
        :param is_fd: Should the Bus be initialized in CAN-FD mode
        :param enable_brs: sets the bitrate_switch flag to use higher transmission speed
        :param f_clock_mhz:  Clock rate in MHz
        :param nom_brp: Clock prescaler for nominal time quantum
        :param nom_tseg1: Time segment 1 for nominal bit rate, that is,
            the number of quanta from the Sync Segment to the sampling point
        :param nom_tseg2: Time segment 2 for nominal bit rate,
            that is, the number of quanta from the sampling point to the end of the bit
        :param nom_sjw: Synchronization Jump Width for nominal bit rate.
            Decides the maximum number of time quanta that the controller
            can resynchronize every bit
        :param data_brp: Clock prescaler for fast data time quantum
        :param data_tseg1: Time segment 1 for fast data bit rate, that is,
            the number of quanta from the Sync Segment to the sampling point
        :param data_tseg2: Time segment 2 for fast data bit rate, that is,
            the number of quanta from the sampling point to the end of the bit.
            In the range (1..16)
        :param data_sjw: Synchronization Jump Width for fast data bit rate
        :param is_extended_id: This flag controls the size of the arbitration_id field
        :param remote_id: id used for transmission
        :param can_filters: iterable used to filter can id on reception
        :param logging_activated: boolean used to disable logfile creation
        :param bus_error_warning_filter: if True filter the PCAN driver warnings
            'Bus error: an error counter' from the logs.
        """
        super().__init__(**kwargs)
        self.interface = interface
        self.channel = channel
        self.state = can.bus.BusState[state.upper()]
        self.trace_path = Path(trace_path)
        self.trace_size = trace_size
        self.bitrate = bitrate
        self.is_fd = is_fd
        self.enable_brs = enable_brs
        self.f_clock_mhz = f_clock_mhz
        self.nom_brp = nom_brp
        self.nom_tseg1 = nom_tseg1
        self.nom_tseg2 = nom_tseg2
        self.nom_sjw = nom_sjw
        self.data_brp = data_brp
        self.data_tseg1 = data_tseg1
        self.data_tseg2 = data_tseg2
        self.data_sjw = data_sjw
        self.is_extended_id = is_extended_id
        self.remote_id = remote_id
        self.can_filters = can_filters
        self.bus = None
        self.logging_activated = logging_activated
        self.raw_pcan_interface = None
        # Set a timeout to send the signal to the GIL to change thread.
        # In case of a multi-threading system, all tasks will be called one after the other.
        self.timeout = 1e-6
        self.trc_count = 0
        self._initialize_trace()

        if bus_error_warning_filter:
            logging.getLogger("can.pcan").addFilter(PcanFilter())

        if self.enable_brs and not self.is_fd:
            log.internal_warning(
                "Bitrate switch will have no effect because option is_fd is set to false."
            )

    def _initialize_trace(self) -> None:
        """Initialize the trace path and check its size

        :raises ValueError: if the trace_path is a file but not a trc file
        """

        # Handle trace path and name
        if self.trace_path.suffix == ".trc":
            self.trace_name = self.trace_path.name
            self.trace_path = self.trace_path.parent
        elif self.trace_path and self.trace_path.suffix == "":
            self.trace_name = None
        elif not self.trace_path:
            self.trace_path = Path.cwd()
            self.trace_name = None
        elif self.trace_path.suffix not in [".trc", ""]:
            raise ValueError(
                f"Trace name {self.trace_path.name} is incorrect, it should be a trc file"
            )

        # Check trace size
        if not 0 < self.trace_size <= 100:
            self.trace_size = 10
            log.internal_warning(
                f"Make sure trace size is between 1 and 100 Mb. Setting trace size to default value "
                f"value : {self.trace_size}."
            )

    def _cc_open(self) -> None:
        """Open a can bus channel, set filters for reception and activate PCAN log."""
        self.bus = can.interface.Bus(
            interface=self.interface,
            channel=self.channel,
            state=self.state,
            bitrate=self.bitrate,
            fd=self.is_fd,
            f_clock_mhz=self.f_clock_mhz,
            nom_brp=self.nom_brp,
            nom_tseg1=self.nom_tseg1,
            nom_tseg2=self.nom_tseg2,
            nom_sjw=self.nom_sjw,
            data_brp=self.data_brp,
            data_tseg1=self.data_tseg1,
            data_tseg2=self.data_tseg2,
            data_sjw=self.data_sjw,
            can_filters=self.can_filters,
        )

        if self.logging_activated and self.raw_pcan_interface is None:
            self.raw_pcan_interface = PCANBasic.PCANBasic()
            self._pcan_configure_trace()

    def _pcan_configure_trace(self) -> None:
        """Configure PCAN dongle to create a trace file.

        If self.trace_path is set, this path will be created, if it does not
        exist and the logfile will be placed there.
        Otherwise it will be logged to the current working directory if a
        default filename, which will be overwritten in successive calls.
        If an error occurs, the trace will not be started and the error logged.
        No exception is thrown in this case.
        """
        pcan_channel = getattr(PCANBasic, self.channel)
        if self.trace_path is None:
            log.internal_warning(
                "No trace path specified, an existing trace will be overwritten."
            )
            pcan_path_argument = PCANBasic.TRACE_FILE_OVERWRITE
        else:
            pcan_path_argument = PCANBasic.TRACE_FILE_DATE | PCANBasic.TRACE_FILE_TIME

        try:
            if self.trace_path is not None:
                if not Path(self.trace_path).exists():
                    Path(self.trace_path).mkdir(parents=True, exist_ok=True)
                    log.internal_info(f"Path {self.trace_path} created")
                self._pcan_set_value(
                    pcan_channel,
                    PCANBasic.PCAN_TRACE_LOCATION,
                    bytes(self.trace_path),
                )
                log.internal_info(
                    f"Tracefile path in PCAN device configured to {self.trace_path}"
                )

            if sys.platform != "darwin":
                log.internal_info("Segmented option of trace file activated.")
                self._pcan_set_value(
                    pcan_channel,
                    PCANBasic.TRACE_FILE_SEGMENTED,
                    PCANBasic.PCAN_PARAMETER_ON,
                )

                if self.trace_size != 10:
                    log.internal_info(f"Trace size set to {self.trace_size} MB.")
                    self._pcan_set_value(
                        pcan_channel, PCANBasic.PCAN_TRACE_SIZE, self.trace_size
                    )
            else:
                log.internal_warning("TRACE_FILE_SEGMENTED deactivated for macos!")

            self._pcan_set_value(
                pcan_channel,
                PCANBasic.PCAN_TRACE_CONFIGURE,
                pcan_path_argument,
            )
            log.internal_info("Tracefile configured")

            self._pcan_set_value(
                pcan_channel, PCANBasic.PCAN_TRACE_STATUS, PCANBasic.PCAN_PARAMETER_ON
            )
            log.internal_info("Trace activated")
            self.trc_count += 1
        except RuntimeError:
            log.error(f"Logging for {self.channel} not activated")
        except OSError as e:
            log.error(f"Can not create log folder for PCAN logs: {e}")
            log.error(f"Logging for {self.channel} not activated")

    def _pcan_set_value(self, channel, parameter, buffer) -> None:
        """Set a value in the PCAN api.

        If this is not successful, a RuntimeError is returned, as well as the
        PCAN error text is logged, if possible.

        :param channel: Channel for PCANBasic.SetValue
        :param parameter: Parameter for PCANBasic.SetValue
        :param buffer: Buffer for PCANBasic.SetValue

        :raises RuntimeError: Raised if the function is not successful
        """
        try:
            result = self.raw_pcan_interface.SetValue(
                channel,
                parameter,
                buffer,
            )
        except Exception as e:
            log.error(f"Exception in call to SetValue: {e}")
            raise RuntimeError("Error configuring logging on PCAN")
        else:
            if result != PCANBasic.PCAN_ERROR_OK:
                _, error_msg = self.raw_pcan_interface.GetErrorText(result)
                log.error(error_msg)
                raise RuntimeError(f"Error configuring logging on PCAN: {result}")

    def _cc_close(self) -> None:
        """Close the current can bus channel and uninitialize PCAN handle."""
        self.bus.shutdown()
        self.bus = None
        if self.logging_activated:
            try:
                result = self.raw_pcan_interface.Uninitialize(PCANBasic.PCAN_NONEBUS)
            except Exception as e:
                log.exception(f"Error in call to Uninitialize: {e}")
            else:
                if result != PCANBasic.PCAN_ERROR_OK:
                    _, error_msg = self.raw_pcan_interface.GetErrorText(result)
                    log.error(error_msg)
            finally:
                self.raw_pcan_interface = None

    def _cc_send(
        self, msg: MessageType, remote_id: Optional[int] = None, **kwargs
    ) -> None:
        """Send a CAN message at the configured id.

        If remote_id parameter is not given take configured ones

        :param msg: data to send
        :param remote_id: destination can id used
        :param kwargs: named arguments
        """

        remote_id = remote_id or self.remote_id

        can_msg = can.Message(
            arbitration_id=remote_id,
            data=msg,
            is_extended_id=self.is_extended_id,
            is_fd=self.is_fd,
            bitrate_switch=self.enable_brs,
        )
        self.bus.send(can_msg)

        log.internal_debug(f"{self} sent CAN Message: {can_msg}, data: {msg}")

    def _cc_receive(
        self, timeout: float = 0.0001
    ) -> Dict[str, Union[bytes, int, None]]:
        """Receive a can message using configured filters.

        :param timeout: timeout applied on reception

        :return: the received data and the source can id
        """
        try:  # Catch bus errors & rcv.data errors when no messages where received
            received_msg = self.bus.recv(timeout=timeout or self.timeout)

            if received_msg is not None:
                frame_id = received_msg.arbitration_id
                payload = received_msg.data
                timestamp = received_msg.timestamp

                log.internal_debug(
                    f"received CAN Message: {frame_id}, {payload}, {timestamp}"
                )
                return {"msg": payload, "remote_id": frame_id, "timestamp": timestamp}
            else:
                return {"msg": None}
        except can.CanError as can_error:
            log.internal_info(
                f"encountered CAN error while receiving message: {can_error}"
            )
            return {"msg": None}
        except Exception:
            log.exception(f"encountered error while receiving message via {self}")
            return {"msg": None}

    # TODO: refactor to use trc reader when new version of python can is release
    def _merge_trc(self) -> None:
        """Merge multiple trc files in one."""

        if isinstance(self.trace_path, str):
            self.trace_path = Path(self.trace_path)

        # Get the lastest trace files corresponding to the number of traces created
        list_of_traces = sorted(self.trace_path.glob("*.trc"), key=os.path.getmtime)[
            -self.trc_count :
        ]

        try:
            if self.trace_name is None:
                # If a log file is not provided, take the fist trace created as result file
                result_trace = list_of_traces[0]
            else:
                # Else write the first trace content in the log file and then remove it
                result_trace = Path(self.trace_path / self.trace_name)
                list_of_traces[0] = shutil.move(
                    str(list_of_traces[0]), str(result_trace)
                )
                list_of_traces[0] = Path(list_of_traces[0])

            # End of the trace header
            first_message_line = 33

            # Get start time of the first trc file
            with list_of_traces[0].open("r") as trc:
                data = trc.read().splitlines(True)

                first_trc_start_time = CCPCanCan._get_trace_start_time(
                    data, first_message_line
                )
                message_idx = len(data[first_message_line:])

            list_of_traces.pop(0)

            # Append all trace files
            for file in list_of_traces:
                with file.open("r") as trc:
                    data = trc.read().splitlines(True)

                    # Get offset between current and first trc file
                    trc_start_time = CCPCanCan._get_trace_start_time(
                        data, first_message_line
                    )
                    offset = trc_start_time - first_trc_start_time

                    # Fix message number and time offset inconstistancies
                    corrected_data = CCPCanCan._fix_merge_inconsistencies(
                        data[first_message_line:], offset, message_idx
                    )
                    message_idx += len(data[first_message_line:])

                with result_trace.open("a") as merged_trc:
                    merged_trc.writelines(corrected_data)
                os.remove(file)

        except IndexError:
            log.internal_warning("No trace to merge")

    @staticmethod
    def _fix_merge_inconsistencies(
        data: List[str], offset: float, message_idx: int
    ) -> List[str]:
        """Fix merge inconsistencies such as message number and time offset

        :param data: can messages to fix
        :param offset: time offset beetween first trace and current trace in milliseconds
        :param message_idx: message number from last trace file

        :return: corrected can messages
        """
        message_number_idx = 7
        time_stamp_idx = 22

        for line_number in range(len(data)):
            message_number = str(line_number + 1 + message_idx)
            line = data[line_number]

            # Format time offset
            time_stamp = round(
                float(line[message_number_idx:time_stamp_idx]) + offset, 3
            )
            time_stamp = "{:10.3f}".format(time_stamp)

            # Fix message number
            data[line_number] = (
                message_number.rjust(message_number_idx)
                + time_stamp.rjust(time_stamp_idx - message_number_idx - 1)
                + line[time_stamp_idx - 1 :]
            )
        return data

    @staticmethod
    def _get_trace_start_time(data: List[str], first_message_line: int) -> float:
        """Get trace start time.

        :param trace: path of the trc file
        :param first_message_line: first line after the header

        :raises ValueError: raised if no start time is found in the trace
        :return: start time in milliseconds
        """
        # Search for the start time in the header of the tace
        for line in data[:first_message_line]:
            if line.find(";$STARTTIME=") != -1:
                start_time = float(line[len(";$STARTTIME=") :])
                return CCPCanCan._convert_peak_format_to_start_time(start_time)
        raise ValueError("No start time was found in the trace file")

    @staticmethod
    def _convert_peak_format_to_start_time(start_time: float) -> float:
        """Get the start time of a trc file in milliseconds since the start of the day
        from the peak start time format

        :param start_time: float using the format bellow (from PEAK CAN)
            Integral part = Number of days that have passed since 30. December 1899.
            Fractional Part = Fraction of a 24-hour day that has elapsed, resolution is 1
                millisecond.

        :return: start time of the trc file in ms since the start of the day
        """
        ms_in_a_day = 86400000
        return (start_time % 1) * ms_in_a_day

    def shutdown(self) -> None:
        """Destructor method."""
        if self.logging_activated:
            self._merge_trc()
