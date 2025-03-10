console.log("OneDesk Ticketing: Mockup ready, bud!");

function showNewTicket() {
    document.getElementById("new-ticket-modal").style.display = "flex";
}

function hideNewTicket() {
    document.getElementById("new-ticket-modal").style.display = "none";
}

document.getElementById("ticket-form").addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Ticket submitted! (This is a mockup—real functionality coming soon.)");
    hideNewTicket();
    e.target.reset();
});