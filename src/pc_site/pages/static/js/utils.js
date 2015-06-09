Date.prototype.pattern=function(fmt) {           
    var o = {           
    "M+" : this.getMonth()+1, //月份           
    "d+" : this.getDate(), //日           
    "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时           
    "H+" : this.getHours(), //小时           
    "m+" : this.getMinutes(), //分           
    "s+" : this.getSeconds(), //秒           
    "q+" : Math.floor((this.getMonth()+3)/3), //季度           
    "S" : this.getMilliseconds() //毫秒           
    };           
    var week = {           
    "0" : "/u65e5",           
    "1" : "/u4e00",           
    "2" : "/u4e8c",           
    "3" : "/u4e09",           
    "4" : "/u56db",           
    "5" : "/u4e94",           
    "6" : "/u516d"          
    };           
    if(/(y+)/.test(fmt)){           
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));           
    }           
    if(/(E+)/.test(fmt)){           
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);           
    }           
    for(var k in o){           
        if(new RegExp("("+ k +")").test(fmt)){           
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));           
        }           
    }           
    return fmt;           
}

function replace_null(obj, rep) {
    return null == obj ? rep : obj;
}

function enable_obj(obj, enable) {
    if (!enable) {
        obj.addClass("disabled");
    } else {
        obj.removeClass("disabled");
    }
}


function judge(val) {
    var cls = "";
    var text = "";
    
    if (val > 80) {
        cls = "text-danger";
        text = "严重抄袭";
    } else if (val > 50) {
        cls = "text-warning";
        text = "抄袭";
    } else if (val > 10) {
        cls = "text-info";
        text = "少量抄袭";
    } else {
        cls = "text-success";
        text = "无抄袭";
    }
    
    return '<td class="' + cls + '">' + text + '</td>';
}

function parse_to_table(data) {
    var ret = "";
    var status_map = ['等待', '分析中', '已完成'];
    var status_class_map = ['text-normal', 'text-info', 'text-success'];
    
    for (i in data) {
        ret += "<tr>";
        row = data[i];
        
        ret += '<td class="' + status_class_map[row['status']] + '">' 
                + status_map[row['status']] + '</td>';
        ret += '<td><a href="' + row['url'] + '" target="_blank">'
                + (null == row['title'] ? row['url'] : row['title'])
                + '</a></td>';
        ret += '<td>' + replace_null(row['author'], '-') + '</td>';
        ret += '<td>' + new Date(row['create_time'] * 1000).pattern("yyyy-MM-dd HH:mm") + '</td>';
        
        if (2 != row['status']) {
            ret += '<td>-</td><td class="text-right">-</td>';
        } else {
	        ret += judge(row['result']);
	        ret += '<td class="text-right">' + ((null == row['result']) ? '-' : (String(row['result']) + '%')) + '</td>';
        }
    }
    
    return ret;
}

function pagination(pages, cur) {
    var ret = "";
    var max_pages = 10;
    
    if (cur < 1) {
        cur = 1;
    } else if (cur > pages) {
        cur = pages;
    }
    
    var show_count = (pages > max_pages) ? max_pages : pages;
    var begin = 0;
    
    if (cur < parseInt(show_count / 2)) {
        begin = 1;
    } else if (cur > pages - parseInt(show_count / 2)) {
        begin = pages - show_count + 1;
    } else {
        begin = cur - parseInt(show_count / 2);
    }
    
    if (begin < 1) begin = 1;
    
    var onclick = 'onclick="page_bar_click(' + String(cur - 1) + ');"';
    
    if (1 == cur) {
        ret += '<li class="disabled"><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>';
    } else {
        ret += '<li><a href="javascript:void(0);" ' + onclick + ' aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>';
    }
    
    for (var i = 0; i < show_count; i++) {
        var num = begin + i;
        onclick = 'onclick="page_bar_click(' + String(num) + ');"';
        
        if (num == cur) {
            ret += '<li class="active"><a href="javascript:void(0);">' + String(num) + '<span class="sr-only">(current)</span></a></li>';
        } else {
            ret += '<li><a href="javascript:void(0);" ' + onclick + '>' + String(num) + '</a></li>';
        }
    }
    
    onclick = 'onclick="page_bar_click(' + String(cur + 1) + ');"';
    if (cur == pages) {
        ret += '<li class="disabled"><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>';
    } else {
        ret += '<li><a href="javascript:void(0); "' + onclick + ' aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>';
    }
    
    return ret;
}

