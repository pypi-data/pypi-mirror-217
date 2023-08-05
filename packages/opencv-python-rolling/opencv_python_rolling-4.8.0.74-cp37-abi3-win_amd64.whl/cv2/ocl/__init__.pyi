import typing


# Enumerations
OCL_VECTOR_OWN: int
OCL_VECTOR_MAX: int
OCL_VECTOR_DEFAULT: int
OclVectorStrategy = int
"""One of [OCL_VECTOR_OWN, OCL_VECTOR_MAX, OCL_VECTOR_DEFAULT]"""


Device_TYPE_DEFAULT: int
DEVICE_TYPE_DEFAULT: int
Device_TYPE_CPU: int
DEVICE_TYPE_CPU: int
Device_TYPE_GPU: int
DEVICE_TYPE_GPU: int
Device_TYPE_ACCELERATOR: int
DEVICE_TYPE_ACCELERATOR: int
Device_TYPE_DGPU: int
DEVICE_TYPE_DGPU: int
Device_TYPE_IGPU: int
DEVICE_TYPE_IGPU: int
Device_TYPE_ALL: int
DEVICE_TYPE_ALL: int
Device_FP_DENORM: int
DEVICE_FP_DENORM: int
Device_FP_INF_NAN: int
DEVICE_FP_INF_NAN: int
Device_FP_ROUND_TO_NEAREST: int
DEVICE_FP_ROUND_TO_NEAREST: int
Device_FP_ROUND_TO_ZERO: int
DEVICE_FP_ROUND_TO_ZERO: int
Device_FP_ROUND_TO_INF: int
DEVICE_FP_ROUND_TO_INF: int
Device_FP_FMA: int
DEVICE_FP_FMA: int
Device_FP_SOFT_FLOAT: int
DEVICE_FP_SOFT_FLOAT: int
Device_FP_CORRECTLY_ROUNDED_DIVIDE_SQRT: int
DEVICE_FP_CORRECTLY_ROUNDED_DIVIDE_SQRT: int
Device_EXEC_KERNEL: int
DEVICE_EXEC_KERNEL: int
Device_EXEC_NATIVE_KERNEL: int
DEVICE_EXEC_NATIVE_KERNEL: int
Device_NO_CACHE: int
DEVICE_NO_CACHE: int
Device_READ_ONLY_CACHE: int
DEVICE_READ_ONLY_CACHE: int
Device_READ_WRITE_CACHE: int
DEVICE_READ_WRITE_CACHE: int
Device_NO_LOCAL_MEM: int
DEVICE_NO_LOCAL_MEM: int
Device_LOCAL_IS_LOCAL: int
DEVICE_LOCAL_IS_LOCAL: int
Device_LOCAL_IS_GLOBAL: int
DEVICE_LOCAL_IS_GLOBAL: int
Device_UNKNOWN_VENDOR: int
DEVICE_UNKNOWN_VENDOR: int
Device_VENDOR_AMD: int
DEVICE_VENDOR_AMD: int
Device_VENDOR_INTEL: int
DEVICE_VENDOR_INTEL: int
Device_VENDOR_NVIDIA: int
DEVICE_VENDOR_NVIDIA: int

KernelArg_LOCAL: int
KERNEL_ARG_LOCAL: int
KernelArg_READ_ONLY: int
KERNEL_ARG_READ_ONLY: int
KernelArg_WRITE_ONLY: int
KERNEL_ARG_WRITE_ONLY: int
KernelArg_READ_WRITE: int
KERNEL_ARG_READ_WRITE: int
KernelArg_CONSTANT: int
KERNEL_ARG_CONSTANT: int
KernelArg_PTR_ONLY: int
KERNEL_ARG_PTR_ONLY: int
KernelArg_NO_SIZE: int
KERNEL_ARG_NO_SIZE: int


# Classes
class Device:
    # Functions
    def __init__(self) -> None: ...

    def name(self) -> str: ...

    def extensions(self) -> str: ...

    def isExtensionSupported(self, extensionName: str) -> bool: ...

    def version(self) -> str: ...

    def vendorName(self) -> str: ...

    def OpenCL_C_Version(self) -> str: ...

    def OpenCLVersion(self) -> str: ...

    def deviceVersionMajor(self) -> int: ...

    def deviceVersionMinor(self) -> int: ...

    def driverVersion(self) -> str: ...

    def type(self) -> int: ...

    def addressBits(self) -> int: ...

    def available(self) -> bool: ...

    def compilerAvailable(self) -> bool: ...

    def linkerAvailable(self) -> bool: ...

    def doubleFPConfig(self) -> int: ...

    def singleFPConfig(self) -> int: ...

    def halfFPConfig(self) -> int: ...

    def endianLittle(self) -> bool: ...

    def errorCorrectionSupport(self) -> bool: ...

    def executionCapabilities(self) -> int: ...

    def globalMemCacheSize(self) -> int: ...

    def globalMemCacheType(self) -> int: ...

    def globalMemCacheLineSize(self) -> int: ...

    def globalMemSize(self) -> int: ...

    def localMemSize(self) -> int: ...

    def localMemType(self) -> int: ...

    def hostUnifiedMemory(self) -> bool: ...

    def imageSupport(self) -> bool: ...

    def imageFromBufferSupport(self) -> bool: ...

    def intelSubgroupsSupport(self) -> bool: ...

    def image2DMaxWidth(self) -> int: ...

    def image2DMaxHeight(self) -> int: ...

    def image3DMaxWidth(self) -> int: ...

    def image3DMaxHeight(self) -> int: ...

    def image3DMaxDepth(self) -> int: ...

    def imageMaxBufferSize(self) -> int: ...

    def imageMaxArraySize(self) -> int: ...

    def vendorID(self) -> int: ...

    def isAMD(self) -> bool: ...

    def isIntel(self) -> bool: ...

    def isNVidia(self) -> bool: ...

    def maxClockFrequency(self) -> int: ...

    def maxComputeUnits(self) -> int: ...

    def maxConstantArgs(self) -> int: ...

    def maxConstantBufferSize(self) -> int: ...

    def maxMemAllocSize(self) -> int: ...

    def maxParameterSize(self) -> int: ...

    def maxReadImageArgs(self) -> int: ...

    def maxWriteImageArgs(self) -> int: ...

    def maxSamplers(self) -> int: ...

    def maxWorkGroupSize(self) -> int: ...

    def maxWorkItemDims(self) -> int: ...

    def memBaseAddrAlign(self) -> int: ...

    def nativeVectorWidthChar(self) -> int: ...

    def nativeVectorWidthShort(self) -> int: ...

    def nativeVectorWidthInt(self) -> int: ...

    def nativeVectorWidthLong(self) -> int: ...

    def nativeVectorWidthFloat(self) -> int: ...

    def nativeVectorWidthDouble(self) -> int: ...

    def nativeVectorWidthHalf(self) -> int: ...

    def preferredVectorWidthChar(self) -> int: ...

    def preferredVectorWidthShort(self) -> int: ...

    def preferredVectorWidthInt(self) -> int: ...

    def preferredVectorWidthLong(self) -> int: ...

    def preferredVectorWidthFloat(self) -> int: ...

    def preferredVectorWidthDouble(self) -> int: ...

    def preferredVectorWidthHalf(self) -> int: ...

    def printfBufferSize(self) -> int: ...

    def profilingTimerResolution(self) -> int: ...

    @classmethod
    def getDefault(cls) -> Device: ...


class OpenCLExecutionContext:
    ...


# Functions
def finish() -> None: ...

def haveAmdBlas() -> bool: ...

def haveAmdFft() -> bool: ...

def haveOpenCL() -> bool: ...

def setUseOpenCL(flag: bool) -> None: ...

def useOpenCL() -> bool: ...


