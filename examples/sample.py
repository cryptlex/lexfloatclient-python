import sys, ctypes, time
import LexFloatClient

# Refer to following link for LexFloarClient API docs:
# https://github.com/cryptlex/lexfloatclient-c/blob/master/examples/LexFloatClient.h
# https://github.com/cryptlex/lexfloatclient-c/blob/master/examples/LexFloatStatusCodes.h

def licence_callback(status):
    if LexFloatClient.StatusCodes.LF_OK == status:
        print("The license lease has renewed successfully.")
    elif LexFloatClient.StatusCodes.LF_E_LICENSE_NOT_FOUND == status:
        print("The license expired before it could be renewed.")
    elif LexFloatClient.StatusCodes.LF_E_LICENSE_EXPIRED_INET == status:
        print("The license expired due to network connection failure.")
    else:
        print("The license renew failed due to other reason. Error code: ", status)

# reference the callback to keep it alive
licence_callback_fn = LexFloatClient.CallbackType(licence_callback)

def get_ctype_string_buffer(size):
    if sys.platform == 'win32':
        return ctypes.create_unicode_buffer(size)
    else:
        return ctypes.create_string_buffer(size)

def get_ctype_string(input):
    if sys.platform == 'win32':
        return ctypes.c_wchar_p(input)
    else:
        return ctypes.c_char_p(input)

def main():    
    # Set the product id
    status = LexFloatClient.SetHostProductId("PASTE_PRODUCT_ID")
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Set the float server
    status = LexFloatClient.SetHostUrl("http://localhost:8090")
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Set the license callback
    status = LexFloatClient.SetFloatingLicenseCallback(licence_callback_fn)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Request license lease
    status = LexFloatClient.RequestFloatingLicense()
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Request license error code: ", status)
        sys.exit(status)
    print("Success! License Acquired. Press enter to get the license metadata...")
    sys.stdin.read(1)
    # Request license metadata
    bufferSize = 256
    buffer = get_ctype_string_buffer(bufferSize)
    status = LexFloatClient.GetHostLicenseMetadata("key1", buffer, bufferSize)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Metadata request error code: ", status)
    else:
        print("Metadata: ", buffer.value)
    print("Press enter to drop the license ...")
    sys.stdin.read(1)
    # Drop license lease
    status = LexFloatClient.DropFloatingLicense()
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Drop license error code: ", status)
        sys.exit(status)
    print("Success! License dropped.")
main()
