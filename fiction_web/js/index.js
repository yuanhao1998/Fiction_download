$(document).ready(function () {
    // 根据是否登录来判断显示热搜或者书架
    if (localStorage.token && localStorage.username){
        $('.login_user').css('display', 'block')
        $('.username').val(localStorage.username)
        // $('.no_login').css('display', 'none')
        $('.data iframe').attr('src', 'bookshelves.html')
    }
    else{
        // $('.login_user').css('display', 'block')
        // $('.username').val(localStorage.username)
        $('.data iframe').attr('src', 'hot.html')
    }
})

//登录
function login(){
    $.ajax({
        url: 'http://127.0.0.1:8000/user/login/',
        type: 'post',
        dataType: 'json',
        data: {
            'username': $('.username').val(),
            'password': $('.password').val()
        },
        success: function (response) {
            if (response.token && response.username) {
                localStorage.token = response.token  // 本地存储  token、username
                localStorage.username = response.username
                $('.login_user').css('display', 'block')
                $('.username').val(response.username)
                $('.no_login').css('display', 'none')
            }
        },
        error: function () {
            alert('登录失败')
        }
    });
}

//切换到热搜页面
function hot(){
    $('.data iframe').attr('src', 'hot.html')
}

//切换到书架页面
function bookshelves(){
    $('.data iframe').attr('src', 'bookshelves.html')
}

//搜索书籍
function search(e){
    console.log(e)
    $.ajax({
        url: 'http://127.0.0.1:8000/search/' + e + '/',
        type: 'get',
        dataType: 'json',
        success: function(response){
            let title = $('.title p');
            title.text(e + ": 搜索结果");
            let data = $("#iframe").contents().find(".data");  //获取子页面的data元素
            data.empty();
            for (let i in response.data){
                data.append('<p>' + '来源：' + i + '</p>');
                for (let j=0; j<response.data[i].length; j++){
                    let list = response.data[i][j]
                    data.append('<div class="book_div">' +
                        '<p class="book_detail"> 书名：' + list.name + '</p>' +
                        '<p class="book_detail"> 分类：' + list.tag + '</p>' +
                        '<p class="book_detail"> 作者：' + list.author + '</p>' +
                        '<p class="book_detail"> 更新：' + list.update + '</p>' +
                        // '<input type="button" onclick="book_detail(' +'\'' +list.href + '\')" value="查看本书"></div>')
                        '<input type="button" onclick="add_bookshelves(' +'\''+ list.name+'\',\''+list.tag+'\',\''+list.author+'\',\''+list.href + '\')" value="添加到书架"></div>')
                }
            }
        },
        error: function(e){
            console.log(e)
            alert('查询失败，请稍后重试')
        }
    })
}