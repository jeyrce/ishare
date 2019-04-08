$(function () {
    //清空输入框
    $('input[name!="csrfmiddlewaretoken"][name!="next"]').val('');

    //提交按钮点击事件
    $('#submit').on('click', function () {
        var email = $('#email').val();
        var pwd = $('#password').val();
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        var next_url = $('input[name="next"]').val();
        //验证邮箱是否是合法邮箱
        //验证账户是否存在
        //验证账户是否可登录
        //都通过则提交数据
        if (!email) {
            $('#email-tip').text('邮箱不能为空').show();
            $('.form-item').addClass('not-valid');
        } else if (!pwd) {
            $('#pwd-tip').text('密码不能为空').show();
            $('.form-item').addClass('not-valid');
        } else {
            $.ajax({

                type: "POST",

                url: "/x/auth/signin",

                data: {
                    email: email,
                    pwd: pwd,
                    csrfmiddlewaretoken: csrf_token
                },
                //回调
                success: function (res) {
                    var code = res["code"];
                    switch (code) {
                        case 0:
                            document.location.href = next_url;
                            break;
                        case -1:
                            $('#email-tip').text(res["msg"]).show();
                            $('.form-item').addClass('not-valid');
                            break;
                        case -2:
                            $('#email-tip').text(res["msg"]).show();
                            $('.form-item').addClass('not-valid');
                            break;
                        case -3:
                            $('#pwd-tip').text(res["msg"]).show();
                            $('.form-item').addClass('not-valid');
                            alert(res["msg"]);
                            break;
                        default: alert('未知错误，清稍后再试!.'); break;
                    }
                }

            });
        }
    });

    //当focus时移除不合法提示
    $('input').on('focus', function () {
        $('.tip').hide();
        $('.form-item').removeClass('not-valid')
    });

});
