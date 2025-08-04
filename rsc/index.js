/* jshint esversion: 9 */

function toggle_fav(element,id){
    
    const raw_favs = localStorage.getItem("favs");
    let favorites = raw_favs ? raw_favs.split(',') : [];
    
    if (favorites.includes(id)) {
        console.log(`removing ${id} from fav`);
        favorites = favorites.filter(id_ => id_ !== id);
        element.classList.remove('isfav');
        console.log("favs",localStorage.getItem("favs"));
    } else {
        console.log(`adding ${id} from fav`);
        favorites.push(id);
        element.classList.add('isfav');
        console.log(localStorage.getItem("favs"));
    }
    console.log("favorites",favorites);
    localStorage.setItem("favs",favorites.join(','));
}


function toggle_ui() {
    let new_theme = localStorage.getItem('ui-theme') === 'dark'? 'light' : 'dark';
    console.log("switch to", new_theme);
    // button
    document.querySelectorAll(`[data-theme]`).forEach(d=>{d.classList.remove("hide");});
    document.querySelector(`[data-theme="${new_theme}"]`).classList.add("hide");
    // stylesheet
    document.querySelectorAll("#style-ui-dark, #style-ui-light").forEach(s=>{s.disabled = true;});
    document.getElementById(`style-ui-${new_theme}`).disabled = false;
    
    localStorage.setItem('ui-theme', new_theme);
}


function init_code_copy_event(){
    document.querySelectorAll("div.code-block div.code-header img.copy").forEach(img => {
        img.addEventListener("click", () => {
            const code = img.closest("div.code-block").querySelector("div.highlight pre");
            if (!code) return;

            navigator.clipboard.writeText(code.textContent).then(() => {
                img.classList.remove("copied");
                void img.offsetWidth; // force reflow
                img.classList.add("copied");
            }).catch(err => {
                img.classList.remove("copied");
                void img.offsetWidth;
                console.error("Copy failed", err);
            });
        });
    });
}

function hasTouch() {
    return 'ontouchstart' in document.documentElement  || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
}





// -------- index

// filter data regarding title
// and edit the title to add `<mark>` for matching substring
function apply_title_query(data){
    let query = document.querySelector("nav input#title").value;
    return data.filter(d => d.title.toLowerCase().includes(query.toLowerCase()))
        .map(d => {
            const dd = { ...d };
            dd.title = dd.title.replace(new RegExp(query, "i"), match => `<mark>${match}</mark>`);
            return dd;
        });
}

// filter data regarding tech
// and edit the tech to add `<mark>` for matching substring
function apply_tech_query(data){
    let query = document.querySelector("nav input#tech").value.trim();
    return data.filter(d => d.tech.toLowerCase().startsWith(query.toLowerCase()))
        .map(d => {
            const dd = { ...d };
            dd.tech = dd.tech.replace(new RegExp(query, "i"), match => `<mark>${match}</mark>`);
            return dd;
        });
}

function create_element(data){
    let a = document.createElement("a");
    a.href = `/${data.id}`
    a.innerHTML = `<p class="title">${data.title}</p><p class="tech">${data.tech}</p><img onclick="toggle_fav(this,'${data.id}'); update_list()" class="favorite ${data.isfav? 'isfav' : ''}" src="rsc/assets/favorite.svg">`;
    return a;
}

function update_list(){
    let data = indexation;

    let main = document.querySelector("main");
    main.innerHTML = "";

    data = apply_tech_query(data);
    if (data.length === 0){
        document.querySelector("#result-separator p").innerHTML = "No results matching 'Tech' filter";
        document.querySelector("input#tech").classList.add("error");
        return;
    }
    document.querySelector("input#tech").classList.remove("error");

    data = apply_title_query(data);
    if (data.length === 0){
        document.querySelector("#result-separator p").innerHTML = "No results matching 'Title' filter";
        document.querySelector("input#title").classList.add("error");
        return;
    }
    document.querySelector("input#title").classList.remove("error");


    document.querySelector("#result-separator p").innerHTML = `${data.length}`;

    let raw_favs = localStorage.getItem('favs');
    let favs = raw_favs ? raw_favs.split(',') : [];
    data.forEach(d=>{
        d.isfav = favs.includes(d.id);
    });

    data.sort((a, b) => {
        if (a.isfav !== b.isfav){
            return a.isfav ? -1 : 1;
        }
        return (a.title + a.tech).localeCompare(b.title + b.tech);
    });

    data.forEach(d => {
        main.appendChild(create_element(d));
    });
}