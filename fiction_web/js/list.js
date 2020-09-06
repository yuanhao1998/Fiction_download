$(document).ready(function () {
    $.ajax({
        url:'http://127.0.0.1:8000/book/list/' + localStorage.book_id + '/',
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function (response){
            let data = $('.data')
            data.empty();
            for (let i in response.data){
                console.log(i)
                data.append('<p  onclick="read(' + response.data[i].chapter_id + ')">' + response.data[i].chapter_name + '</p>')
                data.append('<br>')
            }
        },
        error: function(e) {
            console.log(e)
            if (e.status === 401)
                alert('认证信息过期，请重新登陆！')
            else
                alert('获取内容失败，请稍后再试')
        }
    })
})

function read(chapter_id){
    $('.data iframe', parent.document).attr('src', 'book.html')
    localStorage.chapter_id = chapter_id;
}