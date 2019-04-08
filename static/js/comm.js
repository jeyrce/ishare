$(document).ready(function () {
    //nav     
    var obj = null;
    var As = document.getElementById('starlist').getElementsByTagName('a');
    obj = As[0];
    for (i = 1; i < As.length; i++) {
        if (window.location.href.indexOf(As[i].href) >= 0) obj = As[i];
    }
    obj.id = 'selected';
    //nav
    $("#mnavh").click(function () {
        $("#starlist").toggle();
        $("#mnavh").toggleClass("open");
    });
    //search  
    $(".searchico").click(function () {
        $(".search").toggleClass("open");
    });
    //searchclose 
    $(".searchclose").click(function () {
        $(".search").removeClass("open");
    });
    //banner
    $('#banner').easyFader();
    //nav menu   
    $(".menu").click(function (event) {
        $(this).children('.sub').slideToggle();
    });
    //tab
    $('.tab_buttons li').click(function () {
        $(this).addClass('newscurrent').siblings().removeClass('newscurrent');
        $('.newstab>div:eq(' + $(this).index() + ')').show().siblings().hide();
    });

    //点赞
    $('#like').click(function (event) {
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        like_btn = $('#like');
        var liked = $('input[name="liked"]').val();
        if (liked == 'true') {
            alert('你已经点过赞啦！');
        } else {
            $.ajax({
                type: "POST",
                url: document.location.href,
                data: {
                    csrfmiddlewaretoken: csrf_token
                },
                //回调
                success: function (res) {
                    alert("感谢你的点赞！");
                    //局部刷新点击后的点赞数并标记点赞
                    like_btn.text('很赞哦(' + res["msg"] + ')');
                    $('input[name="liked"]').val('true');
                }
            });
        }
    });

    //打赏文章作者
    $('#dashang').click(function (event) {
        //显示该文章作者的两张打赏码
        console.log('你对作者的赞赏就是作者创作的动力！');
    });
    //复制本文地址
    $('#copy').click(function (event) {
        var author = $('input[name="author"]').val();
        var site = $('input[name="site"]').val();
        var link = $('input[name="link"]').val();
        var str = '-------------------------------------------------\r\n' +
                  '来源:' + site + '\r\n' +
                  '链接:' + link + '\r\n' +
                  '作者:' + author + '\r\n' +
                  '声明:' + '原创著作版权归本站及作者所有，转载引用请注明来源。\r\n' +
                  '-------------------------------------------------\r\n';
        console.log(str);
        executeCopy(str);
        alert('复制本文地址成功！欢迎转载分享！')
    });

    // Copy text as text
    function executeCopy(text) {
        var input = document.createElement('textarea');
        document.body.appendChild(input);
        input.value = text;
        // input.focus();
        input.select();
        document.execCommand('Copy', false);
        input.remove();
    }
});
