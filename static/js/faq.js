const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach((item) => {
    const btn = item.querySelector(".faq-question");
    const popup = item.querySelector(".faq-popup");
    const icon = item.querySelector("div.bg-foreground");

    btn.addEventListener("click", (e) => {
        e.stopPropagation();

        const isOpen = !popup.classList.contains("hidden");

        // Закрыть все остальные
        faqItems.forEach((i) => {
            const otherBtn = i.querySelector(".faq-question");
            const otherPopup = i.querySelector(".faq-popup");
            const otherIcon = i.querySelector("div.bg-foreground");

            otherPopup.classList.add("hidden");
            otherIcon.classList.remove("rotate-90");

            // Восстанавливаем полное округление
            otherBtn.classList.remove("rounded-t-2xl");
            otherBtn.classList.add("rounded-2xl");
        });

        if (!isOpen) {
            popup.classList.remove("hidden");
            icon.classList.add("rotate-90");

            // Убираем нижние закругления у открытого вопроса
            btn.classList.remove("rounded-2xl");
            btn.classList.add("rounded-t-2xl");
        }
    });
});

// Клик вне FAQ закрывает всё
document.addEventListener("click", () => {
    faqItems.forEach((i) => {
        const btn = i.querySelector(".faq-question");
        const popup = i.querySelector(".faq-popup");
        const icon = i.querySelector("div.bg-foreground");

        popup.classList.add("hidden");
        icon.classList.remove("rotate-90");

        // Восстанавливаем закругления
        btn.classList.remove("rounded-t-2xl");
        btn.classList.add("rounded-2xl");
    });
});
