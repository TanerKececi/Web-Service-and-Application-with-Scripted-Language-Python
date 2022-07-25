function validate() {
    var uname = document.forms["loginform"]["uname"].value;
    var pwd = document.forms["loginform"]["pwd"].value;

    if (uname == "") {
      window.alert("Username should be entered");
      return false;
    } else if (pwd == "") {
      window.alert("Password should be entered");
      return false;
    }
  }