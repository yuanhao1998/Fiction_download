function submit(){
    let username = $('.username')
    let password = $('.password')
    let repeat = $('.repeat')
    if (password.val() === repeat.val()){
        $.ajax({
            url: 'http://127.0.0.1:8000/user/registered/',
            type: 'post',
            dataType: 'json',
            data: {
                'username': username.val(),
                'password': password.val(),
                'repeat': repeat.val()
            },
            success: function(response){
                if (response.errno === 0){
                    alert('注册成功！')
                    $('.data iframe', parent.document).attr('src', 'hot.html')
                }
                else{
                    console.log(response)
                    alert('注册失败')
                }
            }
        })
    }
    else
        alert('两次密码输入不一致，请重试')
}