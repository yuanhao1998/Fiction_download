$(document).ready(function () {
    // 展示书架
    $.ajax({
        url: 'http://127.0.0.1:8000/bookshelves/',
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function(response){
            let data = $('.data');
            data.empty();
            for (let i in response){
                data.append(
                    '<div class="book_div">' +
                    '<p class="book_detail"> 书名：' + response[i].book_name + '</p>' +
                    '<p class="book_detail"> 作者：' + response[i].author + '</p>' +
                    '<p class="book_detail"> 已阅读到：' + response[i].chapter_name + '</p>' +
                    '<input type="button" onclick="read('  + response[i].book_id + ',' + response[i].chapter_id + ')" value="继续阅读">' +
                    '</div>'
                )
            }
        },
        error: function(e) {
            console.log(e)
            if (e.status === 401)
                alert('认证信息过期，请重新登陆！')
            else
                alert('获取书架内容失败，请稍后再试')
        }
    });
})

// 阅读书籍
function read(book_id, chapter_id){
    $('.data iframe', parent.document).attr('src', 'book.html')
    localStorage.book_id = book_id;
    localStorage.chapter_id = chapter_id
}