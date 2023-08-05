import cv2
import typing


# Functions
def getBackendName(api: cv2.VideoCaptureAPIs) -> str: ...

def getBackends() -> typing.Sequence[cv2.VideoCaptureAPIs]: ...

def getCameraBackendPluginVersion(api: cv2.VideoCaptureAPIs) -> tuple[str, int, int]: ...

def getCameraBackends() -> typing.Sequence[cv2.VideoCaptureAPIs]: ...

def getStreamBackendPluginVersion(api: cv2.VideoCaptureAPIs) -> tuple[str, int, int]: ...

def getStreamBackends() -> typing.Sequence[cv2.VideoCaptureAPIs]: ...

def getWriterBackendPluginVersion(api: cv2.VideoCaptureAPIs) -> tuple[str, int, int]: ...

def getWriterBackends() -> typing.Sequence[cv2.VideoCaptureAPIs]: ...

def hasBackend(api: cv2.VideoCaptureAPIs) -> bool: ...

def isBackendBuiltIn(api: cv2.VideoCaptureAPIs) -> bool: ...


