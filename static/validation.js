function validateForm(operation) {
  var extension = document.forms["Form"]["filename"].value.split('.');
  if (extension[extension.length - 1] != "pdf") {
    alert("Pleae enter a PDF file only.");
    return false;
  }
  if (operation == 'encrypt') {
    var pass = document.forms["Form"]["password"].value;
    var cpass = document.forms["Form"]["cpassword"].value;
    if (pass != cpass){
      alert("Password does not match. Please try again.");
      return false;
    }
  }
  if (operation == 'change_pass') {
    var pass = document.forms["Form"]["new_password"].value;
    var cpass = document.forms["Form"]["cpassword"].value;
    if (pass != cpass){
      alert("New Password does not match. Please try again.");
      return false;
    }
  }

}
