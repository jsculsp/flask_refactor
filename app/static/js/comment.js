var log = function() {
    console.log(arguments)
}

var bindEventCommentAdd = function() {
    $('#submit').on('click', function() {
        log('click')
        var content = $('#body').val()
        var form = {
            body: content
        }
        var postId = $('li.post').data('id')
        var response = function(r) {
            if (r.success) {
                var t = r.data
                $('.comments').prepend(t)
                $('#body').val('')
                alert('添加成功！')
            } else {
                alert(r.message)
            }
        }
        api.commentAdd(postId, form, response)
    })
}

var bindEvents = function() {
    bindEventCommentAdd()
}

$(document).ready(function() {
    bindEvents()
})