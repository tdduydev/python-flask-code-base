import enum


class ReturnMessageEnum(str, enum.Enum):
    success = "success"
    fail = "fail"
    missing = "missing"
    invalid = "invalid"
    denied = "denied"
    not_json = "not_json"
    exist = "exist"
    not_exist = "not_exist"
    unavailable_language = 'unavailable_language'


return_message = {
    'en': {
        'success': "Request success",
        'not_json': "Request data must be a Json format",
        'fail': "Request fail",
        'missing': "Missing data",
        'invalid': "Data is invalid",
        'denied': "Permission denied",
        'exist': "Object is already exist",
        'not_exist': "Object doesn't exist",
        'unavailable_language': "Input language is not available"
    },
    'vn': {
        'success': "Thành công",
        'fail': "Thất bại",
        'not_json': "Dữ liệu phải thuộc dạng Json",
        'missing': "Thiếu dữ liệu",
        'invalid': "Dữ liệu không đúng",
        'denied': "Quyền truy cập bị từ chối",
        'exist': "Vật thể đang tồn tại",
        'not_exist': "Vật thể không tồn tại",
        'unavailable_language': "Ngôn ngữ "
    }
}
