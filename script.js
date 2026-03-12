// SIGNUP FUNCTION
function signup(){

let newUser = document.getElementById("newuser").value;
let newPass = document.getElementById("newpass").value;

if(newUser=="" || newPass==""){
alert("Please fill all fields");
return;
}

localStorage.setItem("username",newUser);
localStorage.setItem("password",newPass);

alert("Account Created Successfully!");

window.location.href="login.html";

}


// LOGIN FUNCTION
function login(){

let user = document.getElementById("user").value;
let pass = document.getElementById("pass").value;

let savedUser = localStorage.getItem("username");
let savedPass = localStorage.getItem("password");

if(user===savedUser && pass===savedPass){

alert("Login Successful!");

window.location.href="dashboard.html";

}
else{

alert("Wrong Username or Password");

}

}