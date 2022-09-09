async function hideSelect() {
    let select = document.getElementById("audio-format");
    let div = select.parentNode;
    console.log(select);
    console.log(div);
    div.classList.toggle("hidden");
}

async function sendLink() {
    let button = document.getElementById("submit-button");
    let link = document.getElementById("link");
    let loading = document.getElementById("loading");
    let audioVideo = document.getElementById("audio-video").value;
    let options = document.getElementById("audio-format").value.split("-");
    let quality
    let format
    if (audioVideo == "audio" && options[0] !== "best") {
        quality = options[1];
        format = options[0];
    } else {
        quality = "best";
        format = "none";
    }
    if (options[0] == "best") {
        format = "none"
    }

    if (link.classList.contains("hidden") == false) {
        link.classList.toggle("hidden");
    } 
    if (loading.classList.contains("hidden")) {
        loading.classList.toggle("hidden");
    }
    let songTitle = document.getElementById("song-title");
    button.classList.toggle("is-loading");
    songTitle.innerText = "Ripping. Please Wait..."
    let input = document.getElementById("input-form").value;
    let data = {link: input,
                quality: quality,
                format: format,
                audioVideo: audioVideo};
    console.log(options)
    console.log(data)
    const response = await fetch("/get_link", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
    if (response.ok) {
        // let headers = response.headers
        // filename = headers.get("Content-Disposition").split("filename=")[1];
        // cleanFilename = filename.split('"')[1];
        // let blob = await response.blob();
        // let url = URL.createObjectURL(blob);
        let data = await response.json();
        let filename = data["filename"];
        link.href = window.location.href + filename;
        if (link.classList.contains("hidden")) {
            link.classList.toggle("hidden");
        }
        if (loading.classList.contains("hidden") == false) {
            loading.classList.toggle("hidden");
        }
        songTitle.innerText = filename.substring(4);
        button.classList.toggle("is-loading");
    } else {
        if (loading.classList.contains("hidden") == false) {
            loading.classList.toggle("hidden");
        }
        songTitle.innerText = "Rip Failed: Make sure link is not playlist, or try again later...";
        button.classList.toggle("is-loading");
    }
    
    return 1;
};