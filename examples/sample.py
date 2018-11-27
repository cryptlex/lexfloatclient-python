import sys, ctypes, time
import LexFloatClient

# Refer to following link for LexFloarClient API docs:
# https://github.com/cryptlex/lexfloatclient-c/blob/master/examples/LexFloatClient.h
# https://github.com/cryptlex/lexfloatclient-c/blob/master/examples/LexFloatStatusCodes.h

def licence_callback(status):
    if LexFloatClient.StatusCodes.LF_E_LICENSE_EXPIRED == status:
        print("The lease expired before it could be renewed.")
    elif LexFloatClient.StatusCodes.LF_E_LICENSE_EXPIRED_INET == status:
        print("The lease expired due to network connection failure.")
    elif LexFloatClient.StatusCodes.LF_E_SERVER_TIME == status:
        print("The lease expired because Server System time was modified.")
    elif LexFloatClient.StatusCodes.LF_E_TIME == status:
        print("The lease expired because Client System time was modified.")
    else:
        print("The lease expired due to some other reason: ", status)

# reference the callback to keep it alive
licence_callback_fn = LexFloatClient.CallbackType(licence_callback)

def main():    
    handle = ctypes.c_uint()
    # Set the product id
    status = LexFloatClient.GetHandle("PASTE_PRODUCT_ID", ctypes.byref(handle))
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Set the float server
    status = LexFloatClient.SetFloatServer(handle.value, "localhost", 8090)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Set the license callback
    status = LexFloatClient.SetLicenseCallback(handle.value, licence_callback_fn)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Error code: ", status)
        sys.exit(status)
    # Request license lease
    status = LexFloatClient.RequestLicense(handle.value)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Request license error code: ", status)
        sys.exit(status)
    print("Success! License Acquired. Press enter to get the license metadata...")
    sys.stdin.read(1)
    # Request license metadata
    bufferSize = 256
    buffer = ctypes.create_string_buffer(bufferSize)
    status = LexFloatClient.GetLicenseMetadata(handle.value, "key1", buffer, bufferSize)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Metadata request error code: ", status)
    else:
        print("Metadata: ", buffer.value)
    print("Press enter to drop the license ...")
    sys.stdin.read(1)
    # Drop license lease
    status = LexFloatClient.DropLicense(handle)
    if LexFloatClient.StatusCodes.LF_OK != status:
        print("Drop license error code: ", status)
        sys.exit(status)
    print("Success! License dropped.")
    LexFloatClient.GlobalCleanUp()
main()
