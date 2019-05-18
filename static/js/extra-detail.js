$(document).ready(function () {
    //解决文章详情页ueditor代码块宽度超出问题
    $('.syntaxhighlighter').each(function (index, item) {
        var s = $('<div style="overflow-x: auto" class="codeBox"></div>');
        var html = $(item).clone()[0].outerHTML;
        $(item).before(s);
        $(item).remove();
        $('.codeBox').eq(index).html(html);
    });

});
