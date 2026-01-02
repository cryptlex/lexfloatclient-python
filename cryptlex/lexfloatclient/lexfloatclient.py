import ctypes
import json
import functools
import warnings
from cryptlex.lexfloatclient import lexfloatclient_native as LexFloatClientNative
from cryptlex.lexfloatclient.lexfloatstatus_codes import LexFloatStatusCodes
from cryptlex.lexfloatclient.lexfloatclient_exception import LexFloatClientException

callback_list = []

def deprecated(alternative):
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    
    Args:
        alternative (str): Name of the alternative function to use
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"The function {func.__name__}() is deprecated. Use {alternative}() instead.",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

class PermissionFlags:
        LF_USER = 10
        LF_ALL_USERS = 11

class HostLicenseMeterAttribute(object):
    def __init__(self, name, allowed_uses, total_uses, gross_uses):
        self.name = name
        self.allowed_uses = allowed_uses
        self.total_uses = total_uses
        self.gross_uses = gross_uses

class HostProductVersionFeatureFlag(object):
    def __init__(self, name, enabled, data):
        self.name = name
        self.enabled = enabled
        self.data = data

class HostFeatureEntitlement(object):
    def __init__(self, host_feature_entitlement_dict):
        self.feature_name = host_feature_entitlement_dict.get("featureName")
        self.feature_display_name = host_feature_entitlement_dict.get("featureDisplayName")
        self.value = host_feature_entitlement_dict.get("value")
        self.expires_at = host_feature_entitlement_dict.get("expiresAt")


class HostConfig(object):
    def __init__(self, max_offline_lease_duration):
        self.max_offline_lease_duration = max_offline_lease_duration


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
                value (str): string of maximum length 4096 characters with utf-8 encoding

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
    def SetPermissionFlag(flag):
        """Sets the permission flag.
         
         This function must be called on every start of your program after SetHostProductId()
         function in case the application allows borrowing of licenses or system wide activation.

        Args:
                flags : depending on your application's requirements, choose one of 
                the following values: LF_USER, LF_ALL_USERS.
                
                LF_USER: This flag indicates that the application does not require
                admin or root permissions to run.
                
                LF_ALL_USERS: This flag is specifically designed for Windows and should be used 
                for system-wide activations.
        
        Raises:
                LexFloatClientException
        """
        status = LexFloatClientNative.SetPermissionFlag(flag)
        if LexFloatStatusCodes.LF_OK != status:
            raise LexFloatClientException(status)
         
    @staticmethod
    def GetFloatingClientLibraryVersion():
        """Gets the floating client library version.

        Raises:
                LexFloatClientException
        
        Returns:
                str: library version.
        """

        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetFloatingClientLibraryVersion(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)  
     
    @staticmethod
    def GetHostConfig():
        """This function sends a network request to LexFloatServer to get the configuration details.

        Raises:
                LexFloatClientException
        
        Returns:
                HostConfig: host configuration.
        """
        buffer_size = 1024      
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostConfig(buffer, buffer_size)
        if status == LexFloatStatusCodes.LF_OK:
            host_config_json = LexFloatClientNative.byte_to_string(buffer.value)
            if not host_config_json.strip():
                return None
            else:
                host_config = json.loads(host_config_json)
                return HostConfig(host_config["maxOfflineLeaseDuration"])
        else:
            raise LexFloatClientException(status)

    @staticmethod
    @deprecated("GetHostLicenseEntitlementSetName")
    def GetHostProductVersionName():
        """Gets the product version name.

        Raises:
                LexFloatClientException
        
        Returns:
                str: name of the product version.
        """

        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostProductVersionName(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

    @staticmethod
    @deprecated("GetHostLicenseEntitlementSetDisplayName")
    def GetHostProductVersionDisplayName():
        """Gets the product version display name.

        Raises:
                LexFloatClientException
        
        Returns:
                str: display name of the product version.
        """

        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostProductVersionDisplayName(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

    @staticmethod
    @deprecated("GetHostFeatureEntitlement")
    def GetHostProductVersionFeatureFlag(name):
        """Gets the product version feature flag.

        Args:
                name (str): name of the feature flag
                
        Raises:
                LexFloatClientException

        Returns:
                HostProductVersionFeatureFlag: product version feature flag 
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        enabled = ctypes.c_uint()
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostProductVersionFeatureFlag(cstring_name, ctypes.byref(enabled), buffer, buffer_size)
        if status == LexFloatStatusCodes.LF_OK:
            isEnabled = enabled.value > 0
            return HostProductVersionFeatureFlag(name, isEnabled, LexFloatClientNative.byte_to_string(buffer.value))
        else:
            raise LexFloatClientException(status)
        
    @staticmethod
    def GetHostLicenseEntitlementSetName():
        """Gets the name of the entitlement set associated with the LexFloatServer license.

        Raises:
                LexFloatClientException

        Returns:
                str: host license entitlement set name
        """
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostLicenseEntitlementSetName(buffer, buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)
    
    @staticmethod
    def GetHostLicenseEntitlementSetDisplayName():
        """Gets the display name of the entitlement set associated with the LexFloatServer license.

        Raises:
                LexFloatClientException

        Returns:
                str: host license entitlement set display name
        """
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostLicenseEntitlementSetDisplayName(buffer, buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)
    
    @staticmethod
    def GetHostFeatureEntitlements():
        """Gets the feature entitlements associated with the LexFloatServer license.

        Feature entitlements can be linked directly to a license (license feature entitlements) 
        or via entitlement sets. If a feature entitlement is defined in both, the value from 
        the license feature entitlement takes precedence, overriding the entitlement set value.

        Raises:
                LexFloatClientException

        Returns:
                HostFeatureEntitlements[]: list of host feature entitlements
        """
        buffer_size = 4096
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostFeatureEntitlements(buffer, buffer_size)
        if status == LexFloatStatusCodes.LF_OK:
            host_feature_entitlements_json = LexFloatClientNative.byte_to_string(buffer.value)
            if not host_feature_entitlements_json.strip():
                return []
            else:
                host_feature_entitlements = json.loads(host_feature_entitlements_json)
                host_feature_entitlements_list = [HostFeatureEntitlement(feature_detail) for feature_detail in host_feature_entitlements]
                return host_feature_entitlements_list
        else:
            raise LexFloatClientException(status)
        
    @staticmethod
    def GetHostFeatureEntitlement(feature_name):
        """Gets the feature entitlement associated with the LexFloatServer license.

        Feature entitlements can be linked directly to a license (license feature entitlements) 
        or via entitlement sets. If a feature entitlement is defined in both, the value from 
        the license feature entitlement takes precedence, overriding the entitlement set value.

        Raises:
                LexFloatClientException

        Returns:
                HostFeatureEntitlement: host feature entitlement
        """
        cstring_feature_name = LexFloatClientNative.get_ctype_string(feature_name)
        buffer_size = 1024
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostFeatureEntitlement(cstring_feature_name, buffer, buffer_size)
        if status == LexFloatStatusCodes.LF_OK:
            host_feature_entitlement_json = LexFloatClientNative.byte_to_string(buffer.value)
            host_feature_entitlement = json.loads(host_feature_entitlement_json)
            return HostFeatureEntitlement(host_feature_entitlement)
        else:
            raise LexFloatClientException(status)

    @staticmethod
    def GetHostProductMetadata(key):
        """Gets the value of the product metadata.

        Args:
                key (str): metadata key to retrieve the value

        Raises:
                LexFloatClientException

        Returns:
                str: value of metadata for the key
        """
        cstring_key = LexFloatClientNative.get_ctype_string(key)
        buffer_size = 4096
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetHostProductMetadata(
            cstring_key, buffer, buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

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
        buffer_size = 4096
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
                HostLicenseMeterAttribute: values of meter attribute allowed and total uses
        """
        cstring_name = LexFloatClientNative.get_ctype_string(name)
        allowed_uses = ctypes.c_int64()
        total_uses = ctypes.c_uint64()
        gross_uses = ctypes.c_uint64()
        status = LexFloatClientNative.GetHostLicenseMeterAttribute(
            cstring_name, ctypes.byref(allowed_uses), ctypes.byref(total_uses), ctypes.byref(gross_uses))
        if status == LexFloatStatusCodes.LF_OK:
            return HostLicenseMeterAttribute(name, allowed_uses.value, total_uses.value, gross_uses.value)
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
    def GetFloatingClientLeaseExpiryDate():
        """Gets the lease expiry date timestamp of the floating client.

        Raises:
                LexFloatClientException

        Returns:
                int: the timestamp
        """
        leaseExpiryDate = ctypes.c_uint()
        status = LexFloatClientNative.GetFloatingClientLeaseExpiryDate(
            ctypes.byref(leaseExpiryDate))
        if status == LexFloatStatusCodes.LF_OK:
            return leaseExpiryDate.value
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
    def GetFloatingLicenseMode():
        """Gets the mode of the floating license (online or offline).

        Raises:
                LexActivatorException

        Returns:
                ActivationMode: mode of floating license.
        """
        buffer_size = 256
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetFloatingLicenseMode(buffer,buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)   

    @staticmethod
    def GetFloatingClientMetadata(key):
        """Gets the value of the floating client metadata.

        Args:
                key (str): metadata key to retrieve the value

        Raises:
                LexFloatClientException

        Returns:
                str: value of the floating client metadata
        """
        cstring_key = LexFloatClientNative.get_ctype_string(key)
        buffer_size = 4096
        buffer = LexFloatClientNative.get_ctype_string_buffer(buffer_size)
        status = LexFloatClientNative.GetFloatingClientMetadata(
            cstring_key, buffer, buffer_size)
        if status != LexFloatStatusCodes.LF_OK:
            raise LexFloatClientException(status)
        return LexFloatClientNative.byte_to_string(buffer.value)

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
    def RequestOfflineFloatingLicense(lease_duration):
        """Sends the request to lease the license from the LexFloatServer for offline usage.
        
        Args:
                leaseDuration (int): seconds for which the lease should be obtained.
        
        Raises:
                LexFloatClientException
        """
        status = LexFloatClientNative.RequestOfflineFloatingLicense(lease_duration)
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
        elif LexFloatStatusCodes.LF_FAIL == status:
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
