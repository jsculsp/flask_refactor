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
                alertify.alert("评论成功！", function(){
                    alertify.message('评论成功！')
                })
            } else {
                alertify.alert(r.message, function(){
                    alertify.message(r.message)
                })
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