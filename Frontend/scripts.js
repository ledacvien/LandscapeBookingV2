if (typeof window.apiUrl === "undefined") {
  window.apiUrl = "http://127.0.0.1:5000/api";
}

function loadPage(page, script = null) {
  fetch(page)
    .then((response) => response.text())
    .then((html) => {
      document.getElementById("content").innerHTML = html;
      if (script) {
        loadScript(script);
      }
    })
    .catch((error) => {
      console.error("Error loading page:", error);
    });
}

function loadScript(script) {
  const scriptElement = document.createElement("script");
  scriptElement.src = script;
  scriptElement.onload = () => {
    console.log(`${script} loaded successfully.`);
  };
  scriptElement.onerror = () => {
    console.error(`Failed to load ${script}.`);
  };
  document.body.appendChild(scriptElement);
}
