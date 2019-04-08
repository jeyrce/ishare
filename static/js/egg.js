/*
* author: jeeyshe@gmail.com
* date: 2019-04-09 00:34
* description: 埋藏在控制台的彩蛋
* */

//重复n个字符
function repeat(str, n){
    return new Array(n+1).join(str);
}

$(document).ready(function () {
    var str = [
        "%c青春不是年华，而是心境；",
        "%c青春不是桃面，丹唇，柔膝，而是深沉的意志；恢宏的想象；炙热的爱情；青春是生命盎然的涌流。",
        "%c青春气贯长虹，勇锐盖过怯弱，进取压倒苟安。",
        "%c如此锐气，二十后生而有之，六旬男子则更多见。",
        "%c年岁有加，并非垂老，理想丢弃，方堕暮年。",
        "%c岁月悠悠，衰微只及肌肤；热忱抛却，颓废必致灵魂。",
        "%c忧烦，惶恐，丧失自信，定使心灵扭曲，意气如灰。",
        "%c无论年届花甲，抑或二八芳龄，心中皆有生命之欢乐，奇迹之诱惑，孩童般天真久盛不衰。",
        "%c人人心中皆有一处天线，只要你从天上人间接受美好、希望、欢乐、勇气和力量的信号，你就青春永驻，风华常存。",
        "%c一旦天线下堕，锐气便被冰雪覆盖，玩世不恭，自暴自弃油然而生，即使年方二十，实已垂垂老矣；",
        "%c然则只要树起天线，捕捉乐观信号，你就有望在八十高龄告别尘寰时仍青春韶华。"
    ];
    console.log("%c《青春》---塞缪尔•厄尔曼", "color: red;");
    for (var index=0; index<str.length; index++){
        console.log(repeat('-', 85) + '\r\n');
        console.log(str[index], "color: green;");
    }
    console.log(repeat('-', 85) + '\r\n');
    console.log("%c2019-04-09 00:40 https://www.lujianxin.com", "color: green;");
    console.log("%c~既然都发现这个彩蛋了，收藏一下本站呗^o^", "color: red;");
});
