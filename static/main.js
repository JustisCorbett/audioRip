async function hideSelect() {
    select = document.getElementById("audio-format");
    div = select.parentNode;
    console.log(select);
    console.log(div);
    div.classList.toggle("hidden");
}

async function sendLink() {
    link = document.getElementById("link");
    loading = document.getElementById("loading");
    audioVideo = document.getElementById("audio-video").value;

    if (link.classList.contains("hidden") == false) {
        link.classList.toggle("hidden");
    } 
    if (loading.classList.contains("hidden")) {
        loading.classList.toggle("hidden");
    }
    songTitle = document.getElementById("song-title");
    songTitle.innerText = "Ripping. Please Wait..."
    input = document.getElementById("input-form").value;
    data = {link: input};
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
        let headers = response.headers
        filename = headers.get("Content-Disposition").split("filename=")[1];
        cleanFilename = filename.split('"')[1];
        let blob = await response.blob();
        let url = URL.createObjectURL(blob);
        link.href = url;
        link.download = cleanFilename;
        if (link.classList.contains("hidden")) {
            link.classList.toggle("hidden");
        }
        if (loading.classList.contains("hidden") == false) {
            loading.classList.toggle("hidden");
        }
        songTitle.innerText = cleanFilename;
    } else {
        if (loading.classList.contains("hidden") == false) {
            loading.classList.toggle("hidden");
        }
        re = await response.json()
        songTitle.innerText = re["error"];
    }
    return 1;
};