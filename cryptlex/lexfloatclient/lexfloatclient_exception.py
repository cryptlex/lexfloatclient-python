from cryptlex.lexfloatclient.lexfloatstatus_codes import LexFloatStatusCodes


class LexFloatClientException(Exception):
    def __init__(self, code):
        super(LexFloatClientException, self).__init__(
            LexFloatClientException.get_error_message(code))
        self.message = LexFloatClientException.get_error_message(code)
        self.code = code

    @staticmethod
    def get_error_message(code):
        if code == LexFloatStatusCodes.LF_E_PRODUCT_ID:
            return 'The product id is incorrect.'
        if code == LexFloatStatusCodes.LF_E_CALLBACK:
            return 'Invalid or missing callback function.'
        if code == LexFloatStatusCodes.LF_E_HOST_URL:
            return 'Missing or invalid server url.'
        if code == LexFloatStatusCodes.LF_E_TIME:
            return 'Ensure system date and time settings are correct.'
        if code == LexFloatStatusCodes.LF_E_INET:
            return 'Failed to connect to the server due to network error.'
        if code == LexFloatStatusCodes.LF_E_NO_LICENSE:
            return 'License has not been leased yet.'
        if code == LexFloatStatusCodes.LF_E_LICENSE_EXISTS:
            return 'License has already been leased.'
        if code == LexFloatStatusCodes.LF_E_LICENSE_NOT_FOUND:
            return 'License does not exist on server or has already expired.'
        if code == LexFloatStatusCodes.LF_E_LICENSE_EXPIRED_INET:
            return 'License lease has expired due to network error.'
        if code == LexFloatStatusCodes.LF_E_LICENSE_LIMIT_REACHED:
            return 'The server has reached it\'s allowed limit of floating licenses.'
        if code == LexFloatStatusCodes.LF_E_BUFFER_SIZE:
            return 'The buffer size was smaller than required.'
        if code == LexFloatStatusCodes.LF_E_METADATA_KEY_NOT_FOUND:
            return 'The metadata key does not exist.'
        if code == LexFloatStatusCodes.LF_E_METADATA_KEY_LENGTH:
            return 'Metadata key length is more than 256 characters.'
        if code == LexFloatStatusCodes.LF_E_METADATA_VALUE_LENGTH:
            return 'Metadata value length is more than 256 characters.'
        if code == LexFloatStatusCodes.LF_E_FLOATING_CLIENT_METADATA_LIMIT:
            return 'The floating client has reached it\'s metadata fields limit.'
        if code == LexFloatStatusCodes.LF_E_METER_ATTRIBUTE_NOT_FOUND:
            return 'The meter attribute does not exist.'
        if code == LexFloatStatusCodes.LF_E_METER_ATTRIBUTE_USES_LIMIT_REACHED:
            return 'The meter attribute has reached it\'s usage limit.'
        if code == LexFloatStatusCodes.LF_E_PRODUCT_VERSION_NOT_LINKED:
            return 'No product version is linked with the license.'
        if code == LexFloatStatusCodes.LF_E_FEATURE_FLAG_NOT_FOUND:
            return 'The product version feature flag does not exist.'
        if code == LexFloatStatusCodes.LF_E_IP:
            return 'IP address is not allowed.'
        if code == LexFloatStatusCodes.LF_E_CLIENT:
            return 'Client error.'
        if code == LexFloatStatusCodes.LF_E_SERVER:
            return 'Server error.'
        if code == LexFloatStatusCodes.LF_E_SERVER_TIME_MODIFIED:
            return 'System time on server has been tampered with.'
        if code == LexFloatStatusCodes.LF_E_SERVER_LICENSE_NOT_ACTIVATED:
            return 'The server has not been activated using a license key.'
        if code == LexFloatStatusCodes.LF_E_SERVER_LICENSE_EXPIRED:
            return 'The server license has expired.'
        if code == LexFloatStatusCodes.LF_E_SERVER_LICENSE_SUSPENDED:
            return 'The server license has been suspended.'
        if code == LexFloatStatusCodes.LF_E_SERVER_LICENSE_GRACE_PERIOD_OVER:
            return 'The grace period for server license is over.'
        return 'Unknown error!'
