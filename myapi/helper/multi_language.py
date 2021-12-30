import enum


class DictionaryReturnType(str, enum.Enum):
    success = "success"
    fail = "fail"
    missing = "missing"
    invalid = "invalid"
    denied = "denied"


return_message = {
    'en': {
        'success': "Success",
        'fail': "Fail",
        'missing': "Missing data",
        'invalid': "Data is invalid",
        'denied': "Permission denied"
    },
    'vn': {
        'success': "Thành công",
        'fail': "Thất bại",
        'missing': "Thiếu dữ liệu",
        'invalid': "Dữ liệu không đúng",
        'denied': "Quyền truy cập bị từ chối"
    }
}
