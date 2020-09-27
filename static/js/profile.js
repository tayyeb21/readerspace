document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#changepasswordbtn").onclick = (e) => {
        // console.log(e.target);
        e.target.disabled = "disabled"; 
        const oldpassword = document.querySelector("#oldpassword");
        const newpassword = document.querySelector("#newpassword");
        const cnfpassword = document.querySelector("#confirmpassword");
        if(oldpassword.value == "" || newpassword.value == "" || cnfpassword.value == ""){
            e.target.disabled = "";        
            document.querySelector("#errorMessagePassword").innerHTML = "* All fields are compulsory";
        }

        if(newpassword.value === cnfpassword.value){
          fetch("/changePassword", {
            method: "POST",
            headers: new Headers({
              "content-type": "application/json"
            }),
            body: JSON.stringify({
              oldpassword : oldpassword.value,
              newpassword : newpassword.value,
              cnfpassword : cnfpassword.value
            })
          })
          .then(response => response.json())
          .then(data => {
            if(data.success){
              alertify.warning(data.success);              
              $("#changePasswordModal").modal('hide');
            }
            else{
              if(data.message)
                document.querySelector("#errorMessagePassword").innerHTML = data.message;
              else
                alertify.error("Something went wrong");
            }
            
            e.target.disabled = "";
          })
          
        }
        else{
          document.querySelector("#errorMessagePassword").innerHTML = "Password mismatch";
          e.target.disabled = "";
        }
        
        return false;
      };
      document.querySelector("#changeprofilebtn").onclick = (e) => {
        e.target.disabled = "disabled";
        const firstName = document.querySelector("#firstName");
        const middleName= document.querySelector("#middleName");
        const lastName = document.querySelector("#lastName");
        const email = document.querySelector("#email");
        if(firstName.value == "" || lastName.value == "" || email.value == ""){
          document.querySelector("#errorMessageProfile").innerHTML = "* All fields are compulsory";
          e.target.disabled = "";
        }
        else{
          fetch("/editProfile", {
            method: "POST",
            headers: new Headers({
              "content-type": "application/json"
            }),
            body: JSON.stringify({
              firstName : firstName.value,
              middleName: middleName.value,
              lastName  : lastName.value,
              email     : email.value
            })
          })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            if(data.success){
              alertify.warning(data.success);     
              document.querySelector("#userfullname").innerHTML = `${firstName.value} ${middleName.value} ${lastName.value}`;
              document.querySelector("#useremail").innerHTML = `${email.value}`;
              $("#editProfileModal").modal('hide');
            }
            else{
              if(data.message)
                document.querySelector("#errorMessageProfile").innerHTML = data.message;
              else
                alertify.error("Something went wrong");
            }
              e.target.disabled = "";
          })
        }
          
        return false;
    };
})