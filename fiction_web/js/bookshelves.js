$(document).ready(function () {
    // 展示书架
    $.ajax({
        url: 'http://waterberry.cn:8000/bookshelves/',
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function(response){
            if (response.errno === 0){
                let data = $('.data');
                data.empty();
                if (response.data.length === 0){
                    data.append('<p style="text-align: center;font-family: 微软雅黑, serif;font-size: 30px;">空空如也！！！</p>')
                }
                else{
                    for (let i in response.data){
                        data.append(
                            '<div class="book_div">' +
                            '<p class="book_detail"> 书名：' + response.data[i].book_name + '</p>' +
                            '<p class="book_detail"> 作者：' + response.data[i].author + '</p>' +
                            '<p class="book_detail"> 已阅读到：' + response.data[i].chapter_name + '</p>' +
                            '<input type="button" onclick="read('  + response.data[i].book_id + ',' + response.data[i].chapter_id + ')" value="继续阅读">' +
                            '</div>'
                        )
                    }
                }
            }
            else{
                console.log(response)
                alert('请求失败，您可以稍后再试或反馈到管理员')
            }
        },
        error: function(e) {
            console.log(e)
            if (e.status === 401){
                window.localStorage.removeItem('username')
                window.localStorage.removeItem('token')
                alert('需要登陆才能查看书架！')
            }
            else
                alert('获取书架内容失败，请稍后再试')
        }
    });
})

// 阅读书籍
function read(book_id, chapter_id){
    $('.data iframe', parent.document).attr('src', 'book.html')
    localStorage.book_id = book_id;
    localStorage.chapter_id = chapter_id;
}