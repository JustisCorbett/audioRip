async function sendLink() {
    link = document.getElementById("link");
    songTitle = document.getElementById("song-title");
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
    let headers = response.headers
    filename = headers.get("Content-Disposition").split("filename=")[1];
    cleanFilename = filename.split('"')[1];
    let blob = await response.blob();
    let url = URL.createObjectURL(blob);
    link.href = url;
    link.download = cleanFilename;
    songTitle.innerText = cleanFilename;
    console.log(filename);
    return 1;
};