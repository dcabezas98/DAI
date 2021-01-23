function change_mode() {
    var mode = localStorage.getItem("mode") || "classic";
    if (mode=="dark")
	mode="classic";
    else
	mode="dark";

    localStorage.setItem("mode", mode);
    set_mode();
}

function set_mode() {
    var mode = localStorage.getItem("mode") || "classic";
    if (mode=="dark")
	document.body.classList.add("dark-mode");
    else
	document.body.classList.remove("dark-mode");
}

set_mode();
