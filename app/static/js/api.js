var api = {}

api.ajax = function(url, method, form, callback) {
    var request = {
        url: url,
        type: method,
        data: form,
        success: function(response) {
            var r = JSON.parse(response)
            callback(r)
        },
        error: function(err) {
            var r = {
                'success': false,
                'message': '网络错误！'
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.get = function(url, response) {
    api.ajax(url, 'get', {}, response)
}

api.post = function(url, form, response) {
    api.ajax(url, 'post', form, response)
}

// ====================
// 以上是内部函数，内部使用
// --------------------
// 以下是功能函数，外部使用
// ====================

api.commentAdd = function(postId, form, response) {
    url = '/api/post/' + postId
    api.ajax(url, 'post', form, response)
}