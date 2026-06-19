// PROFILE PAGE TAB SWITCHING
let tabs=document.querySelectorAll(".tab");
let sections=document.querySelectorAll(".tab-section");
if (tabs.length>0) {
    tabs.forEach(function(tab){
        tab.addEventListener("click",function(){
            tabs.forEach(function(t){
                t.classList.remove("active");
            });
            sections.forEach(function(section){
                section.classList.remove("active");
            });
            tab.classList.add("active");
            let target=tab.getAttribute("data-tab");
            document.getElementById(target).classList.add("active");
        });
    });
}

// OPEN TAB FROM URL HASH
if(window.location.hash){
    let target=window.location.hash.substring(1);
    tabs.forEach(function(tab){
        tab.classList.remove("active");
    });
    sections.forEach(function(section){
        section.classList.remove("active");
    });
    document.getElementById(target).classList.add("active");
    tabs.forEach(function(tab){
        if(tab.getAttribute("data-tab")===target){
            tab.classList.add("active");
        }
    });
}

// JOB PAGE SEARCH 
let searchInput=document.getElementById("searchInput");
if(searchInput){
    searchInput.addEventListener("keyup",function(){
        let searchValue=searchInput.value.toLowerCase();
        let jobCards=document.querySelectorAll(".job-card");
        jobCards.forEach(function(card){
            let text=card.innerText.toLowerCase();
            if(text.includes(searchValue)){
                card.style.display="block";
            }
            else{
                card.style.display="none";
            }
        });
    });
}

// EDIT PROFILE
let editBtn=document.getElementById("editBtn");
let editForm=document.getElementById("editForm");
let saveBtn=document.getElementById("saveBtn");
if(editBtn){
    editBtn.addEventListener("click",function(){
        editForm.style.display="block";
    });
}

// LOG-OUT MESSAGE
function confirmLogout() {
    let answer=confirm("Are you sure you want to logout?");
    if(answer){
        window.location.href = "/logout";
    }
}