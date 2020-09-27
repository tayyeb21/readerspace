document.addEventListener("DOMContentLoaded", () => {
    const editReview = document.querySelector("#editreview");
    if (editReview != null){
        editReview.onclick = () => {
            /* const isbn = document.querySelector("#isbn").innerText;
            const userRatings = document.querySelector("#user-rating");
            const oldState = userRatings.innerHTML;
            console.log(userRatings);
            const ratings = document.querySelector("#user-ratings");
            console.log(ratings);
            const review = document.querySelector("#user-review").innerText;
            userRatings.innerHTML = "";
            const form = document.createElement('form');
            form.setAttribute("method", "POST");
            form.setAttribute("action", `updateBook/${isbn}`)
            userRatings.appendChild(form);
            for(let i=5; i<0; i--){
                const radio = document.createElement("input");
                radio.type = "radio"
                radio.setAttribute("class", `star star-${i} form-control`);
                radio.id = `rating-${i}`;
                radio.name = "rating";
                radio.value = i;
                radio.setAttribute("required", "required");
                const label = document.createElement("label");
                label.className = `star star-${i}`;
                label.htmlFor = `rating-${i}`;
                form.appendChild(radio);
                form.appendChild(label); 
            
            }*/
            const review = document.querySelector("#user-review").innerText;
            document.querySelector("#edit-review").innerText = review;
        };

    }
    document.querySelector("#updatebtn").onclick = () => {
       /*  if(!document.querySelector("[name=edit-rating]").checked){
            $("#rating-tooltip").tooltip();
            return false;
        } */
    }

});