$(document).ready(function () {
    $.ajax({
        url:'http://waterberry.cn:8000/book/?book_id=' + localStorage.book_id + '&chapter_id='  + localStorage.chapter_id,
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function (response){
            if (response.errno === 0){
                localStorage.chapter_id = response.id;
                let data = $('.data');
                let title = $('.title p');
                title.text(response.title);
                data.empty();
                data.append(response.data);
            }
            else{
                console.log(response)
                alert('请求失败，您可以稍后再试或反馈到管理员')
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

//翻页
function Turn_page(flag){
    let chapter = Number(localStorage.chapter_id) + Number(flag)
    localStorage.chapter_id = chapter
    $.ajax({
        url:'http://waterberry.cn:8000/book/?book_id=' + localStorage.book_id + '&chapter_id='  + chapter,
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function (response){
            if (response.errno === 0){
                let data = $('.data');
                let title = $('.title p');
                title.text(response.title)
                data.empty();
                data.append(response.data)
            }
            else{
                console.log(response)
                alert('请求失败，您可以稍后再试或反馈到管理员')
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
}

//返回目录
function list(){
    $.ajax({
        url:'http://waterberry.cn:8000/book/list/' + localStorage.book_id + '/',
        type: 'get',
        dataType: 'json',
        headers: {
            'Authorization': 'JWT ' + localStorage.token
        },
        success: function (response){
            console.log(response)
        },
        error: function(e) {
            console.log(e)
            if (e.status === 401)
                alert('认证信息过期，请重新登陆！')
            else
                alert('获取内容失败，请稍后再试')
        }
    })
}