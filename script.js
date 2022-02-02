window.onload = () => {
    const messages = document.getElementById("messages");
    fetch("/prev")
        .then((e) => e.json())
        .then((e) => {
            let prev_content = "";
            e.map((t) => (prev_content += `<div> ${t[0]}: ${t[1]} </div>`));
            messages.innerHTML = prev_content;
        });
    const socket = io("http://localhost:8001");
    const login_status = document.getElementById("login_status");

    socket.on("connect", () => {
        console.log("connected");
    });

    socket.on("msg", (e) => {
        const msg = JSON.parse(e);
        messages.innerHTML += `<div> ${msg[0]} : ${msg[1]} </div> `;
    });
    window.socket = socket;
};

function submit() {
    const username = document.getElementById("username");
    const login_status = document.getElementById("login_status");
    fetch(`/login/${username.value}`)
        .then((e) => e.json())
        .then((e) => {
            login_status.innerHTML = `logged in as ${username.value} with token ${e.token}<button > logout </button>`;
            window.token = e.token;
        });
}

function send() {
    const username = document.getElementById("username");
    window.socket.emit(
        "msg",
        `["${window.token}", "${document.getElementById("msg").value}"]`
    );
}
