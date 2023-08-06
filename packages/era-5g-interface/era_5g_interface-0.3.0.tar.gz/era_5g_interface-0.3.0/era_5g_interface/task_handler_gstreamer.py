import logging
import time
from abc import ABC

import cv2

from era_5g_interface.task_handler import TaskHandler, TaskHandlerInitializationFailed


class TaskHandlerGstreamer(TaskHandler, ABC):
    """Abstract class.

    Task handler which takes care of reading the data from Gstreamer
    pipeline with defined parameters. It needs to be inherited to
    implement the store_image method.
    """

    def __init__(self, sid: str, port: int, **kw) -> None:
        """
        Constructor
        Args:
            sid (str): The session id obtained from NetApp client. It is used to
                match the results with the data sender.
            port (int): The port where the Gstreamer pipeline should listen to.
        """

        super().__init__(sid=sid, **kw)
        self.port = port

    def run(self) -> None:
        """The infinite loop which reads the Gstreamer pipeline and pass the
        images to the store_image method, which has to be implemented in the
        child class.

        Raises:
            TaskHandlerInitializationFailed: Raised when the construction of
                Gstreamer pipeline failed
        """

        # pipeline which decodes a h264 stream
        pipeline = (
            f"udpsrc port={self.port} "
            'caps="application/x-rtp,media=(string)video,encoding-name=(string)H264,'
            'payload=(int)96" ! '
            "rtph264depay ! avdec_h264 ! videoconvert ! appsink"
        )

        try:
            logging.info(f"Creating Gstreamer capture on port {self.port}")
            # standard OpenCV VideoCapture connected to the Gstreamer pipeline
            cap = cv2.VideoCapture(pipeline)
            if not cap.isOpened():
                raise TaskHandlerInitializationFailed("VideoCapture was not opened")
            logging.info("Gstreamer capture created")
        except Exception as e:
            logging.error(f"Gstreamer capture failed. {str(e)}")
            # TODO: raise exception?
            exit(1)

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if ret:
                recv_timestamp = time.time_ns()
                # use frame number instead of unknown timestamp
                logging.debug(f"CAP_PROP_POS_MSEC: {int(cap.get(cv2.CAP_PROP_POS_MSEC ))}")
                logging.debug(f"CAP_PROP_POS_FRAMES: {int(cap.get(cv2.CAP_PROP_POS_FRAMES))} {recv_timestamp}")
                timestamp = str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
                self.store_image(
                    {
                        "sid": self.sid,
                        "websocket_id": self.websocket_id,
                        "timestamp": timestamp,
                        "recv_timestamp": recv_timestamp,
                    },
                    frame,
                )
        cap.release()
