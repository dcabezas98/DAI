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

function show_forms(){
    $('#block-name').html("Pokemon");
    $('#block-search').html(`<div class="row">
    <div class="col-md-12">
    <h2>Search:</h2>
    <form class="form-inline mb-1 mt-0" id="search">
        <input name="num" class="form-control" type="number" placeholder="Number">
        <input name="name" class="form-control ml-2" type="text" placeholder="Name">
        <input name="type" class="form-control ml-2" type="text" placeholder="Type">
    <button class="btn btn-success ml-2" onclick="search();">Search</button>
    </form>
</div>
</div>`);
    $('#block-content').html(`<strong id="showing"></strong>
<div class="row mt-2" id="header">
    <div class="col">Nº</div>
    <div class="col">Name</div>
    <div class="col">Image</div>
    <div class="col">Type</div>
    <div class="col">Prev Evol</div>
    <div class="col">Next Evol</div>
    <div class="col"></div>
</div>
<div id="table"></div>`);
}

function show_search(response) {
    table="";
    $("#showing").html("Showing: "+response.length.toString());
    response.forEach(function(element){
	row=`<div class="row" id="instance">`; // Nuevo Pokemon
	row+=`<div class="col">${element.num}</div>`; // Número
	row+=`<div class="col">${element.name}</div>`; // Nombre
	row+=`<div class="col"><img src="${element.img}" width="120" height="120"></img></div>`; // Imagen
	row+=`<div class="col">`; // Tipos
	element.type.forEach(function(t){row+=`${t}<br/>`;});
	row+=`</div>`;
	row+=`<div class="col">`; // Prev evolution
	if(element.hasOwnProperty('prev_evolution')){
	    element.prev_evolution.forEach(function(e){row+=`${e.num}: ${e.name}<br/>`;});
	}
	row+=`</div>`;
	row+=`<div class="col">`; // Next evolution
	if(element.hasOwnProperty('next_evolution')){
	    element.next_evolution.forEach(function(e){row+=`${e.num}: ${e.name}<br/>`;});
	}
	row+=`</div>`;
	row+=`<div class="col">`; // Edit/Delete button
	row+=`<a class="btn btn mt-4" id="editBtn" onclick="delete_pokemon(${element.num});">Delete</a>`;
	row+=`</div>`;
	row+=`</div>`;
	
	table+=row
    });

    $("#table").html(table);
}

function search_all() {
    let url='http://0.0.0.0:5000/api/pokemon';
    var request = $.ajax({
	method: "GET",
	url: url
    });
    request.done(show_search);
}

function search() {
    let url='http://0.0.0.0:5000/api/pokemon?';
    $('#search').find(':input').each(function() {
	url+=$(this).attr('name')+'='+$(this).val()+'&';
	console.log($(this).attr('name'),$(this).val());
    });
    console.log(url);

    var request = $.ajax({
	method: "GET",
	url: url
    });
    request.done(show_search);
}

function delete_pokemon(num) {
    url="http://0.0.0.0:5000/api/pokemon/"+num;
    var request = $.ajax({
	method: "DELETE",
	url: url
    });

    //search_all();
}
