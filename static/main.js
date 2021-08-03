async function sendLink() {
    audioPlayer = document.getElementById("audio-player")
    input = document.getElementById("input-form").value
    data = {link: input}
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
    let blob = new Blob([response.body], {type: response.headers["Content-Type"]});
    audioPlayer.src = URL.createObjectURL(blob);
    console.log(response);
    return response;
}