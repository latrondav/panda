function download(){
    const form=document.getElementById('table');
    html2pdf()
    .from(form)
    .save();
}

function downloadTicket(){
    const ticket=document.getElementById('ticket');
    html2pdf()
    .from(ticket)
    .save();
}


