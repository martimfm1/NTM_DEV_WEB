 // FAQ's starts
 document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const faqItem = question.parentNode;

        document.querySelectorAll('.faq-item').forEach(item => {
            if (item !== faqItem) {
                item.classList.remove('active');
            }
        });

        faqItem.classList.toggle('active');
    });
});
// FAQ's ends

// logout starts
function logout() {
    const response = confirm("Are you sure you want to log out?");
    if (response) {
        alert("Logging out...");
        window.location.href = "/logout";
    } else {
        alert("You cancelled this operation");
    }
}
// logout ends

// hamburguer starts
const toggleButton = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

toggleButton.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    toggleButton.classList.toggle('active');
});
// hamburger ends

// comprar starts
document.getElementById("btn-sell").addEventListener("click", async () => {
    try {
        const response = await fetch("/buy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        if (data.success) {
            alert("Check your message on Discord.");
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error("Request error:", error);
        alert("An error occurred while processing your purchase.");
    }
});
// comprar ends
