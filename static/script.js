function scrollToContact() {
    document.getElementById("contact").scrollIntoView({
        behavior: "smooth"
    });
}

function submitForm() {
    document.getElementById("msg").innerText =
        "Thank you! We will contact you soon.";
    return false; // prevent page reload
}
