from ctypes import *
import os, sys, inspect
import ctypes
import ctypes.util


def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
            and type._type_ != "P"):
        return type
    else:
        return c_void_p


def get_library_path():
    # Get the working directory of this file
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    dir_path = os.path.dirname(os.path.abspath(filename))
    if sys.platform == 'darwin':
        return os.path.join(dir_path, "libLexFloatClient.dylib")
    elif sys.platform == 'linux':
        return os.path.join(dir_path, "libLexFloatClient.so")
    elif sys.platform == 'win32':
        return os.path.join(dir_path, "LexFloatClient.dll")
    else:
        raise TypeError("Platform not supported!")


def load_library(path):
    if sys.platform == 'darwin':
        return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
    elif sys.platform == 'linux':
        return ctypes.cdll.LoadLibrary(path)
    elif sys.platform == 'win32':
        return ctypes.cdll.LoadLibrary(path)
    else:
        raise TypeError("Platform not supported!")

def get_char_type():
    if sys.platform == 'win32':
        return c_wchar_p
    else:
        return c_char_p

library = load_library(get_library_path())

# define types
CSTRTYPE = get_char_type()
STRTYPE = get_char_type()

CallbackType = CFUNCTYPE(UNCHECKED(None), c_uint32)

GetHandle = library.GetHandle
GetHandle.argtypes = [CSTRTYPE, POINTER(c_uint32)]
GetHandle.restype = c_int

SetFloatServer = library.SetFloatServer
SetFloatServer.argtypes = [c_uint32, CSTRTYPE, c_uint16]
SetFloatServer.restype = c_int

SetLicenseCallback = library.SetLicenseCallback
SetLicenseCallback.argtypes = [c_uint32, CallbackType]
SetLicenseCallback.restype = c_int

RequestLicense = library.RequestLicense
RequestLicense.argtypes = [c_uint32]
RequestLicense.restype = c_int

DropLicense = library.DropLicense
DropLicense.argtypes = [c_uint32]
DropLicense.restype = c_int

HasLicense = library.HasLicense
HasLicense.argtypes = [c_uint32]
HasLicense.restype = c_int

FindHandle = library.FindHandle
FindHandle.argtypes = [CSTRTYPE, POINTER(c_uint32)]
FindHandle.restype = c_int

GetLicenseMetadata = library.GetLicenseMetadata
GetLicenseMetadata.argtypes = [c_uint32, CSTRTYPE, STRTYPE, c_uint32]
GetLicenseMetadata.restype = c_int

GlobalCleanUp = library.GlobalCleanUp
GlobalCleanUp.argtypes = []
GlobalCleanUp.restype = c_int


class StatusCodes:
    LF_OK = 0

    LF_FAIL = 1

    LF_E_PRODUCT_ID = 40

    LF_E_CALLBACK = 41

    LF_E_HANDLE = 42

    LF_E_SERVER_ADDRESS = 43

    LF_E_SERVER_TIME = 44

    LF_E_TIME = 45

    LF_E_INET = 46

    LF_E_NO_FREE_LICENSE = 47

    LF_E_LICENSE_EXISTS = 48

    LF_E_LICENSE_EXPIRED = 49

    LF_E_LICENSE_EXPIRED_INET = 50

    LF_E_BUFFER_SIZE = 51

    LF_E_METADATA_KEY_NOT_FOUND = 52

    LF_E_SERVER = 70

    LF_E_CLIENT = 71
