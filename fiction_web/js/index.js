$(document).ready(function () {
    // 根据是否登录来判断显示热搜或者书架
    if (localStorage.token && localStorage.username){
        $('.login_user').css('display', 'block')
        $('.username').val(localStorage.username)
        $('.no_login').css('display', 'none')
        $('.data iframe').attr('src', 'bookshelves.html')
    }
    else{
        $('.no_login').css('display', 'block')
        $('.login_user').css('display', 'none')
        $('.data iframe').attr('src', 'hot.html')
    }
})

//登录
function login(){
    $.ajax({
        url: 'http://waterberry.cn:8000/user/login/',
        type: 'post',
        dataType: 'json',
        data: {
            'username': $('.username').val(),
            'password': $('.password').val()
        },
        success: function (response) {
            if (response.errno === 0){
                if (response.token && response.username) {
                    localStorage.token = response.token  // 本地存储  token、username
                    localStorage.username = response.username
                    $('.login_user').css('display', 'block')
                    $('.username').val(response.username)
                    $('.no_login').css('display', 'none')
                }
            }
            else{
                console.log(response)
                alert('登录失败')
            }
        },
        error: function () {
            alert('登录失败')
        }
    });
}

//退出登陆
function logout(){
    window.localStorage.removeItem('username')
    window.localStorage.removeItem('token')
    window.location.reload()
    alert('退出成功')
}

//切换到注册页面
function registered(){
    $('.data iframe').attr('src', 'registered.html')
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
        url: 'http://waterberry.cn:8000/search/' + e + '/',
        type: 'get',
        dataType: 'json',
        success: function(response){
            if (response.errno === 0){
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
                            '<input type="button" onclick="window.parent.add_bookshelves(' +'\''+ list.name+'\',\''+list.tag+'\',\''+list.author+'\',\''+list.href + '\')" value="添加到书架"></div>')
                    }
                }
            }
            else{
                console.log(response)
                alert('请求失败，您可以稍后再试或反馈到管理员')
            }
        },
        error: function(e){
            console.log(e)
            alert('查询失败，请稍后重试')
        }
    })
}

//添加到书架
function add_bookshelves(book_name,tags,author,href){
    $.ajax({
        url:'http://waterberry.cn:8000/bookshelves/',
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
            if (e.status === 401){
                window.localStorage.removeItem('username')
                window.localStorage.removeItem('token')
                alert('需要登陆才能添加到书架！')
            }
            else
                alert('添加失败，请稍后重试')
        }
    })
}