hacked = function () {
    alert('hacked');
}
window.addEventListener('load',
    function () {
        var f = document.querySelector("form");
        f.setAttribute("onsubmit", "hacked()");
    },
    false
);
