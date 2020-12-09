function checkCookie(){
    var username = document.cookie.split('=')[0];
    //var user=getCookie("cname");
//    alert(username)
    if (username =="kd" || username =="test" || username =="pm" || username ==""){
//        ("欢迎 " + username + " 再次访问");
       alert("返回登录界面登录")
        //清除所有cookie函数
        var cookie = document.cookie.split(';');
        for (var i = 0; i < cookie.length; i++) {
        var chip = cookie[i],
                entry = chip.split("="),
                name = entry[0];
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        }
       window.location.href='login.html';
    }
    else {
    //    window.location.href='login.html';
    //    alert("返回登录界面登录");
          if (username!="" && username!=null){
            setCookie("username",username,30);
        }
    }
}

