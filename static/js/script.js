// Left Eye Picture Preview JS
let uploadButton=document.getElementById("upload-button");
let chosenImage=document.getElementById("chosen-img");
let fileName=document.getElementById("file-name");
var left_image_data = "";
// var left_image_name = "";
let rightEyeResult=document.getElementById("right-eye-result")

uploadButton.onchange=()=>{
    document.getElementById("input-heading").style.display = "none";
    // document.getElementById("input-heading").innerText= "   ";
    // left_image_name = this.value;
    let reader1=new FileReader();
    reader1.readAsDataURL(uploadButton.files[0]);
    console.log(uploadButton.files[0]);
    reader1.onload=()=>{
        left_image_data = reader1.result;
        chosenImage.setAttribute("src",reader1.result)
    }
}

// Right Eye Picture Preview JS
let uploadButton2=document.getElementById("upload-button2");
let chosenImage2=document.getElementById("chosen-img2");
let fileName2=document.getElementById("file-name2");
// var right_image_name = "";
var right_image_data = "";

uploadButton2.onchange=()=>{
    document.getElementById("ip2").style.display = "none";
    // document.getElementById("ip2").innerText = "   ";
    // right_image_name = this.value;
    let reader2=new FileReader();
    reader2.readAsDataURL(uploadButton2.files[0]);
    console.log(uploadButton2.files[0]);
    reader2.onload=()=>{
        right_image_data = reader2.result;
        chosenImage2.setAttribute("src",reader2.result)
    }
}

// Left Eye Caption Input Logic
let fig1_caption=document.getElementById("file-name");
// let fig1_captionInput=document.getElementById("left-eye-picture-caption-input");

// fig1_captionInput.oninput=()=>{
//     fig1_caption.innerHTML=fig1_captionInput.value;
// }

// function inputFunc(){
//     fig1_caption.innerHTML=fig1_captionInput.value;
// }

// fig1_captionInput.addEventListener("mouseenter", (e) => {
//     fig1_caption.innerHTML=fig1_captionInput.value;
//     console.log(fig1_captionInput.value)
//   });

// Left Eye Caption Input Logic
let fig2_caption=document.getElementById("file-name2");
// let fig2_captionInput=document.getElementById("right-eye-picture-caption-input");

// fig2_captionInput.oninput=()=>{
//     fig2_caption.innerHTML=fig2_captionInput.value;
// }

// function changeLogin(){

//     var username_enter_main_page = document.forms["myForm"]["username_enter_main_page"].value;
//     var password_enter_main_page = document.forms["myForm"]["password_enter_main_page"].value;
//     if(username_enter_main_page.value == "doctor" && password_enter_main_page.value == "54321"){
//         fetch("models_page", {
//             method: "GET",
//             headers: {
//               "X-CSRFToken": getCookie("csrftoken"),
//             }
//         });
//     }else{
//         alert("Username or Password is incorrect.")
//     }

// }

function changereg(){
    console.log('ok')
    location.href = "report.html";
}

