async function sendLink() {
    audioPlayer = document.getElementById("audio-player");
    link = document.getElementById("link");
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
    let blob = await response.blob();
    let url = URL.createObjectURL(blob);
    audioPlayer.src = url;
    link.href = url;
    console.log(blob);
    return 1;
}