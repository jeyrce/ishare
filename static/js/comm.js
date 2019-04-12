$(document).ready(function () {
    // //nav
    // var obj = null;
    // var As = document.getElementById('starlist').getElementsByTagName('a');
    // obj = As[0];
    // for (i = 1; i < As.length; i++) {
    //     if (window.location.href.indexOf(As[i].href) >= 0) obj = As[i];
    // }
    // obj.id = 'selected';
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
            layer.msg('你已经点过赞啦！七天内不能重复点赞哦')
        } else {
            $.ajax({
                type: "POST",
                url: document.location.href,
                data: {
                    csrfmiddlewaretoken: csrf_token
                },
                //回调
                success: function (res) {
                    layer.msg('感谢你的点赞！作者将会更加努力写作');
                    //局部刷新点击后的点赞数并标记点赞
                    like_btn.text('很赞哦(' + res["msg"] + ')');
                    $('input[name="liked"]').val('true');
                }
            });
        }
    });

//打赏文章作者
    $('#dashang').click(function (event) {
        var art_id = $('input[name="blog_id"]').val();
        //获取作者打赏码
        $.ajax({
            type: "GET",
            url: '/x/art/dsm/',
            data: {
                'art_id': art_id
            },
            //回调
            success: function (res) {
                //显示该文章作者的两张打赏码
                layer.photos({
                    photos: res,
                    //切换图片时回调
                    tab: function (pic, layero) {
                        if (pic["pid"] == "alipay") {
                            layer.msg('当前是支付宝打赏码，可切换为微信', {time: 2000}, function () {
                            });
                        } else {
                            layer.msg('当前是微信打赏码，可切换为支付宝', {time: 2000}, function () {
                            });
                        }
                    }
                });
            }
        });
    });

//复制本文地址
    $('#copy').click(function (event) {
        var author = $('input[name="author"]').val();
        var site = $('input[name="site"]').val();
        var link = $('input[name="link"]').val();
        var str =
            '来源:' + site + '\r\n' +
            '作者:' + author + '\r\n' +
            '声明:' + '原创著作版权归本站及作者所有，转载引用请注明来源。\r\n' +
            '-------------------------------------------------\r\n' +
            '链接:' + link + '\r\n';
        console.log(str);
        executeCopy(str);
        layer.msg('复制本文永久链接成功，欢迎转载分享！');
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




