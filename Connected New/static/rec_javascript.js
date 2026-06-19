// LOG-OUT MESSAGE
function confirmLogout() {
    let answer=confirm("Are you sure you want to logout?");
    if(answer){
        window.location.href = "/logout";
    }
}
/*profile*/
function editprofile() {
            document.getElementById("profileView").style.display = "none";
            document.getElementById("editForm").style.display = "block";
        }

        function cancelEdit() {
            document.getElementById("editForm").style.display = "none";
            document.getElementById("profileView").style.display = "block";
        }

        function saveProfile(event) {
            event.preventDefault();

            alert("Profile updated successfully!");

            document.getElementById("editForm").style.display = "none";
            document.getElementById("profileView").style.display = "block";
        }

/*applicants*/

function updateStatus(id){

    let select =
        document.getElementById("select" + id);

    let status =
        document.getElementById("status" + id);

    status.innerText = select.value;

    status.className = "status " +
        select.value.toLowerCase();

    alert("Status updated successfully!");
}
function logout(){
    alert("Logged out successfully!");
    window.location.href = "login.html";
}