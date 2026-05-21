async function getVideoInfo(){

    const url = document.getElementById("videoUrl").value;

    if(url === ""){
        alert("Paste YouTube URL");
        return;
    }

    const response = await fetch("/video-info", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            url:url
        })

    });

    const data = await response.json();

    if(data.error){
        alert(data.error);
        return;
    }

    document.getElementById("thumbnail").src = data.thumbnail;

    document.getElementById("title").innerText = data.title;

    document.getElementById("preview").classList.remove("hidden");
}


async function downloadVideo(){

    const url = document.getElementById("videoUrl").value;

    window.location.href = "/download?url=" + encodeURIComponent(url);
}
