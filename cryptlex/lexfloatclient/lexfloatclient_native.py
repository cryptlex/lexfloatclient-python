from ctypes import *
import os
import sys
import platform
import inspect
import subprocess
import ctypes
import ctypes.util


def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
            and type._type_ != "P"):
        return type
    else:
        return c_void_p


def is_os_64bit():
    return platform.machine().endswith('64')

def get_arch():
    is_64bits = sys.maxsize > 2**32
    machine = platform.machine().lower()
    if 'arm' in machine or 'aarch64' in machine:
        if is_64bits:
            return 'arm64'
        else:
            return 'armhf'
    elif is_64bits:
        return 'x86_64'
    else:
        return 'x86'


def is_musl():
    command = ['ldd', '--version']
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
    if 'musl' in output:
        return True
    return False

def get_library_path():
    compiler = 'gcc'
    arch = get_arch()
    # Get the working directory of this file
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    dir_path = os.path.dirname(os.path.abspath(filename))
    # dir_path = os.getcwd()
    if sys.platform == 'darwin':
        return os.path.join(dir_path, "libs/macos/"+arch+"/libLexFloatClient.dylib")
    elif sys.platform.startswith('linux'):
        if(is_musl()):
            compiler = 'musl'
        return os.path.join(dir_path, "libs/linux/"+compiler+"/"+arch+"/libLexFloatClient.so")
    elif sys.platform == 'win32':
        return os.path.join(dir_path, "libs/win32/"+arch+"/LexFloatClient.dll")
    else:
        raise TypeError("Platform not supported!")


def load_library(path):
    if sys.platform == 'darwin':
        return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
    elif sys.platform.startswith('linux'):
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


def get_ctype_string_buffer(size):
    if sys.platform == 'win32':
        return ctypes.create_unicode_buffer(size)
    else:
        return ctypes.create_string_buffer(size)


def get_ctype_string(input):
    if sys.platform == 'win32':
        return ctypes.c_wchar_p(input)
    else:
        return ctypes.c_char_p(input.encode('utf-8'))


def byte_to_string(input):
    if sys.platform == 'win32':
        return input
    else:
        return input.decode('utf-8')


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

GetProductVersionName = library.GetProductVersionName
GetProductVersionName.argtypes = [STRTYPE,c_uint32]
GetProductVersionName.restype = c_int

GetProductVersionDisplayName = library.GetProductVersionDisplayName
GetProductVersionDisplayName.argtypes = [STRTYPE,c_uint32]
GetProductVersionDisplayName.restype = c_int

GetProductVersionFeatureFlag = library.GetProductVersionFeatureFlag
GetProductVersionFeatureFlag.argtypes = [CSTRTYPE, POINTER(c_uint32), STRTYPE, c_uint32]
GetProductVersionFeatureFlag.restype = c_int

GetHostLicenseMetadata = library.GetHostLicenseMetadata
GetHostLicenseMetadata.argtypes = [CSTRTYPE, STRTYPE, c_uint32]
GetHostLicenseMetadata.restype = c_int

GetHostLicenseMeterAttribute = library.GetHostLicenseMeterAttribute
GetHostLicenseMeterAttribute.argtypes = [CSTRTYPE, POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32)]
GetHostLicenseMeterAttribute.restype = c_int

GetHostLicenseExpiryDate = library.GetHostLicenseExpiryDate
GetHostLicenseExpiryDate.argtypes = [POINTER(c_uint32)]
GetHostLicenseExpiryDate.restype = c_int

GetFloatingClientMeterAttributeUses = library.GetFloatingClientMeterAttributeUses
GetFloatingClientMeterAttributeUses.argtypes = [CSTRTYPE, POINTER(c_uint32)]
GetFloatingClientMeterAttributeUses.restype = c_int

RequestFloatingLicense = library.RequestFloatingLicense
RequestFloatingLicense.argtypes = []
RequestFloatingLicense.restype = c_int

DropFloatingLicense = library.DropFloatingLicense
DropFloatingLicense.argtypes = []
DropFloatingLicense.restype = c_int

HasFloatingLicense = library.HasFloatingLicense
HasFloatingLicense.argtypes = []
HasFloatingLicense.restype = c_int

IncrementFloatingClientMeterAttributeUses = library.IncrementFloatingClientMeterAttributeUses
IncrementFloatingClientMeterAttributeUses.argtypes = [CSTRTYPE, c_uint32]
IncrementFloatingClientMeterAttributeUses.restype = c_int

DecrementFloatingClientMeterAttributeUses = library.DecrementFloatingClientMeterAttributeUses
DecrementFloatingClientMeterAttributeUses.argtypes = [CSTRTYPE, c_uint32]
DecrementFloatingClientMeterAttributeUses.restype = c_int

ResetFloatingClientMeterAttributeUses = library.ResetFloatingClientMeterAttributeUses
ResetFloatingClientMeterAttributeUses.argtypes = [CSTRTYPE]
ResetFloatingClientMeterAttributeUses.restype = c_int

