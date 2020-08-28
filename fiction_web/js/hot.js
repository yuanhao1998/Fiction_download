$(document).ready(function () {
    // 展示热搜
    $.ajax({
        url: 'http://127.0.0.1:8000/hot/',
        type: 'get',
        success: function(response){
            let data = $('.data');
            for (let i=0; i<response.data.length; i++){
                data.append('<p class="book" onclick="window.parent.search(this.innerText)"> ' + response.data[i].book_name + '</p>')
            }
        },
        error: function() {
            alert('获取热搜数据失败，请反馈给管理员')
        }
    });
})

//查看书籍
function book_detail(href){
    $.ajax({
        url: 'http://127.0.0.1:8000/search/detail/?href=' + href,
        type: 'get',
        dataType: 'json',
        success: function(response) {
            console.log(response)
            let data = $('.data');
            data.empty()
            data.append(response.data)
        },
        error: function(e){
            console.log(e)

        }
    })
}

//添加到书架
function add_bookshelves(book_name,tags,author,href){
    $.ajax({
        url:'http://127.0.0.1:8000/bookshelves/',
        type: 'post',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        data: {
            "book_name": book_name,
            "tags": tags,
            "author": author,
            "href": href
        },
        success: function(response){
            switch(response.errno){
                case 0:
                    alert('添加成功,请在书架查看');
                    break;
                case 4003:
                    alert('此书籍已添加到您的书架')
                    break;
                default:
                    console.log(response)
                    alert('添加失败，请稍后重试')
            }
        },
        error: function(e){
            console.log(e)
            alert('添加失败，请稍后重试')
        }

    })
}