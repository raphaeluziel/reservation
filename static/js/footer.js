const password=document.querySelector("#passWordField");
const showPassWordToggle=document.querySelector(".showPassWordToggle");

const handleToggleInput = (e) => {
 
  if (showPassWordToggle.textContent === "Show Password"){
    showPassWordToggle.textContent = "Hide Password";
    passWordField.setAttribute("type",'text');

  } else {
    showPassWordToggle.textContent = "Show Password";
    passWordField.setAttribute("type",'password');
  }
 console.log("Testing")
};


showPassWordToggle.addEventListener('click',handleToggleInput);

