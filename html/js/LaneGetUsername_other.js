function getUsername(){
    var username = "other";
    //var user=getCookie("cname");
    //alert("username:" + username)
    var user = document.getElementById('user');
    var user1 = document.getElementById('user1');
    user.value = username
    user1.value = username
    //alert("user.value:" + user.value)
    //alert("user1.value:" + user1.value)
//    if (username == "" || username =="kd" || username == "test" || username == "pm"){
    if (username == "" ){
//        ("欢迎 " + username + " 再次访问");
	alert("username:" + username)
       alert("给你看一眼，然后就回去吧")
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
//        window.location.href='login.html';
     //   alert("欢迎 " + username + " 再次访问");
          if (username!="" && username!=null){
            setCookie("username",username,30);
        }
    }
}
