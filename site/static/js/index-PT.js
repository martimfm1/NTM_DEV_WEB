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
      const resposta = confirm("Tens a certeza que queres sair?");
      if (resposta) {
          alert("A sair...");
          window.location.href = "/logout";
      } else {
          alert("Cancelaste esta operação");
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
          const response = await fetch("/comprar", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
          });
          const data = await response.json();
          if (data.success) {
              alert("Verifique sua mensagem no Discord.");
          } else {
              alert(`Erro: ${data.message}`);
          }
      } catch (error) {
          console.error("Erro na requisição:", error);
          alert("Ocorreu um erro ao processar sua compra.");
      }
  });
  //comprar ends
