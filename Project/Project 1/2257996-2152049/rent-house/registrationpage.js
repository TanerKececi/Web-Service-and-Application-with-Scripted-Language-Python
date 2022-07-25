function validate() {
    var uname = document.forms["registrationform"]["uname"].value;
    var pwd = document.forms["registrationform"]["pwd"].value;
    var name = document.forms["registrationform"]["name"].value;
    var email = document.forms["registrationform"]["email"].value;
    var pnum = document.forms["registrationform"]["pnum"].value;

    if (uname == "") {
      window.alert("Username should be entered");
      return false;
    } else if (pwd == "") {
      window.alert("Password should be entered");
      return false;
    } else if (name == "") {
      window.alert("Full name should be entered");
      return false;
    } else if (email == "") {
      window.alert("Email should be entered");
      return false;
    } else if (pnum == "") {
      window.alert("Phone number should be entered");
      return false;
    }
  }