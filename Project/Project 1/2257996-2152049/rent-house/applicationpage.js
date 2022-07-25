function AdCreate() {
    var form = document.getElementById("adcreate");
    if (form.style.display == "none") {
      form.style.display = "inline";
    } else {
      form.style.display = "none";
    }
  }
  function validate() {
    var sname = document.forms["createAdform"]["sname"].value;
    var noOfbedrooms = document.forms["createAdform"]["noOfbedrooms"].value;
    var mfee = document.forms["createAdform"]["mfee"].value;

    if (sname == "") {
      window.alert("Street name should be entered");
      return false;
    } else if (noOfbedrooms == "") {
      window.alert("Number of bedrooms should be entered");
      return false;
    } else if (mfee == "") {
      window.alert("Monthly fee should be entered");
      return false;
    }
  }