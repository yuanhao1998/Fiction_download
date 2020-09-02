$(document).ready(function () {
    // 展示热搜
    $.ajax({
        url: 'http://127.0.0.1:8000/hot/',
        type: 'get',
        success: function(response){
            if (response.errno === 0){
                let data = $('.data');
                for (let i=0; i<response.data.length; i++){
                    data.append('<p class="book" onclick="window.parent.search(this.innerText)"> ' + response.data[i] + '</p>')
                }
            }
            else{
                console.log(response)
                alert('请求失败，您可以稍后再试或反馈到管理员')
            }
        },
        error: function() {
            alert('获取热搜数据失败，您可以反馈到管理员')
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
