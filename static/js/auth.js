$(function () {
    //清空输入框
    $('input').val('');

    //提交按钮点击事件
    $('#submit').on('click', function () {
        //验证邮箱是否是合法邮箱
        //验证账户是否存在
        //验证账户是否可登录
        //都通过则提交数据
        $('#email-tip').text('请输入合法邮箱').show();
        $('#pwd-tip').text('密码或用户名错误').show();
        $('.form-item').addClass('not-valid')
    });

    //当focus时移除不合法提示
    $('input').on('focus', function () {
        $('.tip').hide();
        $('.form-item').removeClass('not-valid')
    });

    //提交数据
    function submit() {
        var email = $('#email').val();
        var pwd = $('#password').val();
        var csrf_token = $('#csrf_token').val();
    }
});
