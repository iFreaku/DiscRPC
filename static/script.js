document.getElementById("rpcForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const buttons = [];
    document.querySelectorAll("#buttonsContainer .button").forEach((btn) => {
        const label = btn.querySelector("input[name='button_label']").value;
        const url = btn.querySelector("input[name='button_url']").value;
        if (label && url) buttons.push({ label, url });
    });

    const rpcData = {
        appid: document.getElementById("appid").value,
        details: document.getElementById("details").value,
        state: document.getElementById("state").value,
        large_text: document.getElementById("large_text").value,
        large_image: document.getElementById("image_url").value,
        // buttons: buttons,
    };
    

    // const imageFile = document.getElementById("large_image").files[0];
    var imageUrl = document.getElementById("image_url").value;

    // if (imageFile) {
    //     const uploadData = new FormData();
    //     uploadData.append("file", imageFile);
    //     const response = await fetch("/upload_image", {
    //         method: "POST",
    //         body: uploadData,
    //     });
    //     const result = await response.json();
    //     if (result.status === "success") {
    //         console.log(result);
    //         imageUrl = `${result.image_url}`;
    //         rpcData.large_image = imageUrl;
    //     }
    //     else {
    //         console.error(result);
    //     }
    // } else if (imageUrl) {
    rpcData.large_image = imageUrl;
    // }

    const response = await fetch("/update_rpc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(rpcData),
    });

    const result = await response.json();
    alert(result.message);
});

document.getElementById("addButton").addEventListener("click", () => {
    const button = document.createElement("div");
    button.className = "button";
    button.innerHTML = `
        <input type="text" name="button_label" placeholder="Button Label">
        <input type="url" name="button_url" placeholder="Button URL">
        <button type="button" class="removeButton">Remove</button>
    `;
    document.getElementById("buttonsContainer").appendChild(button);
    button.querySelector(".removeButton").addEventListener("click", () => {
        button.remove();
    });
});

document.getElementById("terminateRpc").addEventListener("click", async () => {
    const response = await fetch("/terminate_rpc", { method: "POST" });
    const result = await response.json();
    alert(result.message);
});
