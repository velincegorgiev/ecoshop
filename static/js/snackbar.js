function showSnackbar(text, hex) {
    var x = document.getElementById("snackbar");
    $("#snackbar").css({"backgroundColor":hex});
    x.innerHTML = text;
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
    console.log("snackbar_show");
}