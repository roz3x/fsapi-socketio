window.onload = () => {
    const socket = io("http://localhost:8001");
    const messages = document.getElementById("messages");
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
        });
}

function send() {
    const username = document.getElementById("username");
    window.socket.emit(
        "msg",
        `["${username.value}", "${document.getElementById("msg").value}"]`
    );
}
