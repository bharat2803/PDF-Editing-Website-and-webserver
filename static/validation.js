function validateForm(operation) {
  var extension = document.getElementById("filename").value.split('.');
  if (extension[extension.length - 1] != "pdf") {
    alert("Please enter a PDF file only.");
    return false;
  }
  if (operation == 'encrypt') {
    var pass = document.getElementById("password").value;
    var cpass = document.getElementById("cpassword").value;
    if (pass != cpass){
      alert("Password does not match. Please try again.");
      return false;
    }
  }
  if (operation == 'password-change') {
    var pass = ddocument.getElementById("new-password").value;
    var cpass = document.getElementById("cpassword").value;
    if (pass != cpass){
      alert("New Password does not match. Please try again.");
      return false;
    }
  }

}
