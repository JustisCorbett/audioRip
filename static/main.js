async function sendLink() {
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
    console.log(JSON.stringify(data));
    return response.json();
}