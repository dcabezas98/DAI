days=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

function printTime() {
    var d=new Date();
    document.getElementById("date").innerHTML=days[d.getDay()]+" "+d.getDate()+" "+months[d.getMonth()]+" "+d.getFullYear()+", "+d.getHours().toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
    })+":"+d.getMinutes().toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
    })+":"+d.getSeconds().toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
    });
}

setInterval(printTime, 1000); // Actualiza cada 1000 milisegundos
