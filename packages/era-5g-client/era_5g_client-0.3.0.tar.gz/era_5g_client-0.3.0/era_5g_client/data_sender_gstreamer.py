import cv2
import numpy as np


class DataSenderGStreamer:
    """Class which setups gstreamer connection to the NetApp allowing to send
    image frames using the OpenCV VideoWriter."""

    def __init__(self, host: str, gstreamer_port: int, fps: float, width: int, height: int, threads: int = 1) -> None:
        """Constructor.

        Args:
            host (str): ip address or hostname of the NetApp interface
            gstreamer_port (int): the port assigned for gstreamer communication
            fps (float): the requested FPS of the h264 stream
            threads (int): the number of threads to be used to encode the h264 stream.
                Defaults to 1
        """

        self.host = host
        self.gstreamer_port = gstreamer_port
        self.fps = fps
        self.threads = threads
        self.width = width
        self.height = height

        # default pipeline for sending h264 encoded stream
        # ultrafast and zero latency params for near real-time processing
        pipeline = (
            "appsrc is-live=true ! videoconvert ! "
            "x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true "
            f"threads={self.threads} key-int-max=15 intra-refresh=true ! h264parse ! "
            f"rtph264pay ! udpsink host={self.host} port={self.gstreamer_port}"
        )
        self.out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, fps, (width, height), True)
        # TODO: How to check valid VideoWriter?
        if not self.out.isOpened():
            raise Exception("Cannot open VideoWriter pipeline")
        # self.out.set(cv2.VIDEOWRITER_PROP_QUALITY, 10)

    def send_image(self, frame: np.ndarray) -> None:
        self.out.write(frame)
        # TODO: How to check valid write?
