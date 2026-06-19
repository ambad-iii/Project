function approve(id)
{
    document.getElementById(id).innerHTML = "Approved";
}

function suspend(id)
{
    document.getElementById(id).innerHTML = "Suspended";
}

function confirmLogout() {
    let answer=confirm("Are you sure you want to logout?");
    if(answer){
        window.location.href = "/logout";
    }
}