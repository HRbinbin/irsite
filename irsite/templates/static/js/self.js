// JavaScript Document
function validatorNull() { //判断空值
	var t = document.getElementById("searchnull");
	if (t.value.trim() == "") {
		alert("搜索词不能为空！");
		t.focus();
		return false;
	}
	console.log(t.valueOf());
	return true;
}