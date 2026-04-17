/** @type {WebSocket} */
var ws

function onWsMessage(ws, event) {
    console.log(event)
}

function initSender() {
    document.getElementById("sender-send").addEventListener("click", sendMessage)
}

function sendMessage() {
    const message = document.getElementById("sender-message").value
    const recipient = document.getElementById("sender-recipient").value
    ws.send(JSON.stringify({
        "type": "send",
        "msg": message,
        "to": recipient
    }))
}

window.addEventListener("load", () => {
    ws = new WebSocket("/ws")
    ws.addEventListener("message", onWsMessage)
    initSender()
})