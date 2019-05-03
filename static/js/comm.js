/**
 * 2019-04-01 杰西
 * 一个后端程序员写的js~~~将就着看吧
 *
 */

var HOST = 'https://www.lujianxin.com';

var videoIds = [
    'XMTY3MDgyMjg2OA',//妹子演唱告白气球
    'XMjY3MzgzODg0',//炎心时光，layer默认
];

$(document).ready(function () {
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

    //文章点赞
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

    //公告页替换点赞视频小彩蛋
    $('#about-me').click(function (event) {
        var videoId = Math.floor((Math.random() * videoIds.length));
        //iframe层-多媒体
        layer.open({
            type: 2,
            title: false,
            area: ['630px', '360px'],
            shade: 0.8,
            closeBtn: 0,
            shadeClose: true,
            content: '//player.youku.com/embed/' + videoIds[videoId]
            // content: 'http://player.youku.com/embed/XMTY3MDgyMjg2OA'
        });
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
        var str;
        if (!site || !author || !link) {
            str = 'https://www.lujianxin.com';
        } else {
            str =
                '来源:' + site + '\r\n' +
                '作者:' + author + '\r\n' +
                '声明:' + '原创著作版权归本站及作者所有，转载引用请注明来源。\r\n' +
                '-------------------------------------------------\r\n' +
                '链接:' + link + '\r\n';
        }
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

    //获取提交链接表单
    $('.green').click(function (event) {
        //获取表单
        $.ajax({
            type: 'GET',
            url: '/x/link/add',
            success: function (res) {
                //页面层-自定义
                layer.open({
                    type: 1,
                    title: false,
                    closeBtn: 0,
                    shadeClose: true,
                    content: res['text']
                });
            }
        });
    });

    //友链点击
    $('.goto').click(function (event) {
        var uri = this.id;
        $.ajax({
            type: 'GET',
            url: '/x/goto/',
            async: true,
            data: {
                'uri': uri
            },
        });
        var new_page = uri + '?source=' + HOST;
        window.open(new_page, '_blank');
    });

    //搜索框聚焦清空
    $('#keyboard').focus(function (event) {
        this.value = '';
    });

    //我要投稿点击
    $('#tougao').click(function (event) {
        //投稿提示
        var tips = '<div style="padding: 30px; line-height: 22px; background-color: #393D49; color: #fff; font-weight: 300;">' +
            '<h2>作者须知：</h2><br>' +
            '<b>0、</b>本站作者账号采用非对称加密，全程不存储明文密码，当你修改密码后，就连我也不知道你的密码，请放心使用。如果密码忘了，可以通过登录页面的重置链接进行邮件重置，全程我也是不参与的，请放心！<br><br>' +
            '<b>1、</b>本站已开启审核，不接受存在违反法律法规、传递不正确价值观的言论、其他低质量作品的投稿。<br><br>' +
            '<b>2、</b>本站优先置顶、推荐原创内容，转载文章必须指明出处。<br><br>' +
            '<b>3、</b>作者需遵守国家法律法规、地方政策，对作品版权及其他纠纷负责。<br><br>' +
            '<b>其他未尽事宜请阅读本站公告</b></div>';
        //示范一个公告层
        layer.open({
            type: 1,
            title: false, //不显示标题栏
            closeBtn: false,
            shadeClose: true,
            area: '400px;',
            shade: 0.7,
            id: 'iWrite', //设定一个id，防止重复弹出
            resize: false,
            btn: ['已有作者账号', '选择邮件投稿'],
            btnAlign: 'c',
            moveType: 1, //拖拽模式，0或者1
            content: tips,
            yes: function (x) {
                layer.closeAll();
                window.open('/xauth', '_blank');
            }
        });
    });

    //服务器维护提示
    $('#upgrading').click(function (event) {
        layer.msg('<h1>服务器正在维护</h1>服务器维护期间无法登录作者后台，敬请谅解!', {
            time: 3000, //3s后自动关闭
        });
    })

});

