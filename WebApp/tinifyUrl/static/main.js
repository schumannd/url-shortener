
const onSubmit = () => {
  document.getElementById('output').value = 'processing...'
  const { protocol, host } = window.location;
  const baseUrl = `${protocol}//${host}/`;
  const url = document.getElementById('url').value;
  fetch(`${baseUrl}shorten-url`, {
    method:'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: url})
    })
    .then(async response => {
      const responseJson = await response.json()
      const shortUrl = `${baseUrl}${responseJson.code}`
      document.getElementById('output').innerHTML = `Your shortened URL is: <br /><a href="${shortUrl}">${shortUrl}</a>`;
    });
}

const handleKeyPress = (e) => {
  const key=e.keyCode || e.which;
  if (key == 13) {
     onSubmit();
  }
}

window.onload = () => {
  document.getElementById('submitButton').onclick = onSubmit;
  document.getElementById('url').onkeypress = handleKeyPress;
};