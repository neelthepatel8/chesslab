ERROR_TYPE_NODATA = 'err-no-data'
ERROR_TYPE_NOPOSITION = 'err-no-pos'
ERROR_TYPE_NOPROMOTE_TYPE = 'err-no-promote-type'

RESPONSE_ERROR_DATA = {
    'type': 'error',
    'data': None,
    'error': {
        'type': ERROR_TYPE_NODATA,
        'message': 'No data provided!'
    },
}

RESPONSE_ERROR_POSITION = {
    'type': 'error',
    'data': None,
    'error': {
        'type': ERROR_TYPE_NOPOSITION,
        'message': 'No position provided!'
    },
}

RESPONSE_ERROR_PROMOTE_TYPE = {
    'type': 'error',
    'data': None,
    'error': {
        'type': ERROR_TYPE_NOPROMOTE_TYPE,
        'message': 'No promotion type provided!'
    },
}