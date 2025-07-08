
function writedate() {
    dt = new Date();
    d = document.getElementById('date')
    d.innerHTML = "Date: -" + dt.toGMTString()
    setInterval(writedate, 1)

}