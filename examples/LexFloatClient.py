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

SetHostProductId = library.SetHostProductId
SetHostProductId.argtypes = [CSTRTYPE]
SetHostProductId.restype = c_int

SetHostUrl = library.SetHostUrl
SetHostUrl.argtypes = [CSTRTYPE]
SetHostUrl.restype = c_int

SetFloatingLicenseCallback = library.SetFloatingLicenseCallback
SetFloatingLicenseCallback.argtypes = [CallbackType]
SetFloatingLicenseCallback.restype = c_int

SetFloatingClientMetadata = library.SetFloatingClientMetadata
SetFloatingClientMetadata.argtypes = [CSTRTYPE, CSTRTYPE]
SetFloatingClientMetadata.restype = c_int

GetHostLicenseMetadata = library.GetHostLicenseMetadata
GetHostLicenseMetadata.argtypes = [CSTRTYPE, STRTYPE, c_uint32]
GetHostLicenseMetadata.restype = c_int

GetHostLicenseExpiryDate = library.GetHostLicenseExpiryDate
GetHostLicenseExpiryDate.argtypes = [POINTER(c_uint32)]
GetHostLicenseExpiryDate.restype = c_int

RequestFloatingLicense = library.RequestFloatingLicense
RequestFloatingLicense.argtypes = []
RequestFloatingLicense.restype = c_int

DropFloatingLicense = library.DropFloatingLicense
DropFloatingLicense.argtypes = []
DropFloatingLicense.restype = c_int

HasFloatingLicense = library.HasFloatingLicense
HasFloatingLicense.argtypes = []
HasFloatingLicense.restype = c_int


class StatusCodes:
    
    LF_OK = 0

    LF_FAIL = 1

    LF_E_PRODUCT_ID = 40

    LF_E_CALLBACK = 41

    LF_E_HOST_URL = 42

    LF_E_TIME = 43

    LF_E_INET = 44

    LF_E_NO_LICENSE = 45

    LF_E_LICENSE_EXISTS = 46

    LF_E_LICENSE_NOT_FOUND = 47

    LF_E_LICENSE_EXPIRED_INET = 48

    LA_E_LICENSE_LIMIT_REACHED = 49

    LF_E_BUFFER_SIZE = 50

    LF_E_METADATA_KEY_NOT_FOUND = 51

    LF_E_METADATA_KEY_LENGTH = 52

    LF_E_METADATA_VALUE_LENGTH = 53

    LF_E_FLOATING_CLIENT_METADATA_LIMIT = 54

    LF_E_IP = 60

    LF_E_CLIENT = 70

    LF_E_SERVER = 71

    LF_E_SERVER_TIME_MODIFIED = 72

    LF_E_SERVER_LICENSE_NOT_ACTIVATED = 73

    LF_E_SERVER_LICENSE_EXPIRED = 74

    LF_E_SERVER_LICENSE_SUSPENDED = 75

    LF_E_SERVER_LICENSE_GRACE_PERIOD_OVER = 76
