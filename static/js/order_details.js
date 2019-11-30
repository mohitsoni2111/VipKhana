function changeClass(status) {
    var i, max;
    if (status < 4)
        max = status
    else if (status == 5)
        max = 4
    else if (status == 4)
        max = 2
    else
        max = 5

    for (i = 1; i <= max; i++) {
        document.getElementById(i).className = "progtrckr-done";
    }
}