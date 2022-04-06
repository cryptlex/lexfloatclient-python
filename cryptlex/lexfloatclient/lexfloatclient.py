import ctypes
from cryptlex.lexfloatclient import lexfloatclient_native as LexFloatClientNative
from cryptlex.lexfloatclient.lexfloatstatus_codes import LexFloatStatusCodes
from cryptlex.lexfloatclient.lexfloatclient_exception import LexFloatClientException

callback_list = []


class LicenseMeterAttribute(object):
    def __init__(self, name, allowed_uses, total_uses, gross_uses):
        self.name = name
        self.allowed_uses = allowed_uses
        self.total_uses = total_uses
        self.gross_uses = gross_uses

class ProductVersionFeatureFlag(object):
    def __init__(self, name, enabled, data):
        self.name = name
        self.enabled = enabled
        self.data = data

class LexFloatClient:
    @staticmethod
    def SetHostProductId(product_id):
        """Sets the product id of your application.

        Args:
                product_id (str): the unique product id of your application as mentioned on the product page in the dashboard

        Raises:
                LexFloatClientException
        """
        cstring_product_id = LexFloatClientNative.get_ctype_string(product_id)
        status = LexFloatClientNative.SetHostProductId(cstring_product_id)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def SetHostUrl(host_url):
        """Sets the network address of the LexFloatServer.

        The url format should be: http://[ip or hostname]:[port]

        Args:
                host_url (str): url string having the correct format

        Raises:
                LexFloatClientException
        """
        cstring_host_url = LexFloatClientNative.get_ctype_string(host_url)
        status = LexFloatClientNative.SetHostUrl(cstring_host_url)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def SetFloatingLicenseCallback(license_callback):
        """Sets the renew license callback function.

        Whenever the license lease is about to expire, a renew request is sent to
        the server. When the request completes, the license callback function
        gets invoked with one of the following status codes:

        LF_OK, LF_E_INET, LF_E_LICENSE_EXPIRED_INET, LF_E_LICENSE_NOT_FOUND,
        LF_E_CLIENT, LF_E_IP, LF_E_SERVER, LF_E_TIME,
        LF_E_SERVER_LICENSE_NOT_ACTIVATED,LF_E_SERVER_TIME_MODIFIED,
        LF_E_SERVER_LICENSE_SUSPENDED, LF_E_SERVER_LICENSE_EXPIRED,
        LF_E_SERVER_LICENSE_GRACE_PERIOD_OVER

        Args:
                license_callback (Callable[int]]): callback function

        Raises:
                LexFloatClientException
        """
        license_callback_fn = LexFloatClientNative.CallbackType(
            license_callback)
        callback_list.append(license_callback_fn)
        status = LexFloatClientNative.SetFloatingLicenseCallback(
            license_callback_fn)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def SetFloatingClientMetadata(key, value):
        """Sets the floating client metadata.

        The metadata appears along with the license details of the license in
        LexFloatServer dashboard.

        Args:
                key (str): string of maximum length 256 characters with utf-8 encoding
                value (str): string of maximum length 256 characters with utf-8 encoding

        Raises:
                LexFloatClientException
        """
        cstring_key = LexFloatClientNative.get_ctype_string(key)
        cstring_value = LexFloatClientNative.get_ctype_string(value)
        status = LexFloatClientNative.SetFloatingClientMetadata(
            cstring_key, cstring_value)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def GetProductVersionName():
        """Gets the product version name.

        Raises:
                LexFloatClientException
        
        Returns:
                str: name of the product version.
        """

        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetProductVersionName(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

    @staticmethod
    def GetProductVersionDisplayName():
        """Gets the product version display name.

        Raises:
                LexFloatClientException
        
        Returns:
                str: display name of the product version.
        """

        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetProductVersionDisplayName(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

    @staticmethod
    def GetProductVersionFeatureFlag(name):
        """Gets the product version feature flag.

        Args:
                name (str): name of the feature flag
                
        Raises:
                LexFloatClientException

        Returns:
                ProductVersionFeatureFlag: product version feature flag 
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        enabled = ctypes.c_uint()
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetProductVersionFeatureFlag(cstring_name, ctypes.byref(enabled), buffer, buffer_size)
        if status == LexFloatStatusCodes.LF_OK:
            isEnabled = enabled.value > 0
            return ProductVersionFeatureFlag(name, isEnabled, LexFloatClientNative.byte_to_string(buffer.value))
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def GetHostLicenseMetadata(key):
        """Get the value of the license metadata field associated with the
        LexFloatServer license key.

        Args:
                key (str): metadata key to retrieve the value

        Raises:
                LexFloatClientException

        Returns:
                str: value of metadata for the key
        """
        cstring_key = LexFloatClientNative.get_ctype_string(key)
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostLicenseMetadata(
            cstring_key, buffer, buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

    @staticmethod
    def GetHostLicenseMeterAttribute(name):
        """Gets the license meter attribute allowed uses, total uses and gross uses associated 
        with the LexFloatServer license.

        Args:
                name (str): name of the meter attribute

        Raises:
                LexFloatClientException

        Returns:
                LicenseMeterAttribute: values of meter attribute allowed and total uses
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        allowed_uses = ctypes.c_uint()
        total_uses = ctypes.c_uint()
        gross_uses = ctypes.c_uint()
        status = LexFloatClientNative.GetHostLicenseMeterAttribute(
            cstring_name, ctypes.byref(allowed_uses), ctypes.byref(total_uses), ctypes.byref(gross_uses))
        if status == LexFloatStatusCodes.LF_OK:
            return LicenseMeterAttribute(name, allowed_uses.value, total_uses.value, gross_uses.value)
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def GetHostLicenseExpiryDate():
        """Gets the license expiry date timestamp of the LexFloatServer license.

        Raises:
                LexFloatClientException

        Returns:
                int: the timestamp
        """
        expiry_date = ctypes.c_uint()
        status = LexFloatClientNative.GetHostLicenseExpiryDate(
            ctypes.byref(expiry_date))
        if status == LexFloatStatusCodes.LF_OK:
            return expiry_date.value
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def GetFloatingClientMeterAttributeUses(name):
        """Gets the meter attribute uses consumed by the floating client.

        Args:
                name (str): name of the meter attribute

        Raises:
                LexFloatClientException

        Returns:
                int: value of meter attribute uses by the activation
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        uses = ctypes.c_uint()
        status = LexFloatClientNative.GetFloatingClientMeterAttributeUses(
            cstring_name, ctypes.byref(uses))
        if status == LexFloatStatusCodes.LF_OK:
            return uses.value
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def RequestFloatingLicense():
        """Sends the request to lease the license from the LexFloatServer.

        Raises:
                LexFloatClientException
        """
        status = LexFloatClientNative.RequestFloatingLicense()
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def DropFloatingLicense():
        """Sends the request to the LexFloatServer to free the license.

        Call this function before you exit your application to prevent zombie licenses.

        Raises:
                LexFloatClientException
        """
        status = LexFloatClientNative.DropFloatingLicense()
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def HasFloatingLicense():
        """Checks whether any license has been leased or not.

        Raises:
                LexFloatClientException

        Returns:
                bool: True, False
        """
        status = LexFloatClientNative.HasFloatingLicense()
        if LexFloatStatusCodes.LF_OK == status:
            return True
        elif LexFloatStatusCodes.LF_E_NO_LICENSE == status:
            return False
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def IncrementFloatingClientMeterAttributeUses(name, increment):
        """Increments the meter attribute uses of the floating client.

        Args:
                name (str):  name of the meter attribute
                increment (int): the increment value

        Raises:
                LexFloatClientException
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        status = LexFloatClientNative.IncrementFloatingClientMeterAttributeUses(
            cstring_name, increment)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def DecrementFloatingClientMeterAttributeUses(name, decrement):
        """Decrements the meter attribute uses of the floating client.

        Args:
                name (str): name of the meter attribute
                decrement (int): the decrement value

        Raises:
                LexFloatClientException
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        status = LexFloatClientNative.DecrementFloatingClientMeterAttributeUses(
            cstring_name, decrement)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)

    @staticmethod
    def ResetFloatingClientMeterAttributeUses(name):
        """Resets the meter attribute uses of the floating client.

        Args:
                name (str): name of the meter attribute

        Raises:
                LexFloatClientException
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        status = LexFloatClientNative.ResetFloatingClientMeterAttributeUses(
            cstring_name)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)
