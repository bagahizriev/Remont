document.addEventListener("DOMContentLoaded", function () {
    const phoneInput = document.getElementById("phone");
    if (!phoneInput) return;

    phoneInput.addEventListener("input", onPhoneInput);
    phoneInput.addEventListener("focus", onPhoneFocus);
    phoneInput.addEventListener("blur", onPhoneBlur);

    function onPhoneFocus() {
        if (!this.value) {
            this.value = "+7 (";
        }
    }

    function onPhoneBlur() {
        if (this.value === "+7 (" || this.value === "+7") {
            this.value = "";
        }
    }

    function onPhoneInput(e) {
        const input = e.target;
        const numbers = input.value.replace(/\D/g, "");

        // Ограничиваем максимум 11 цифр (7 + 10 цифр)
        let formatted = "+7";
        if (numbers.length > 1) {
            formatted += " (" + numbers.slice(1, 4);
        }
        if (numbers.length >= 5) {
            formatted += ") " + numbers.slice(4, 7);
        }
        if (numbers.length >= 8) {
            formatted += "-" + numbers.slice(7, 9);
        }
        if (numbers.length >= 10) {
            formatted += "-" + numbers.slice(9, 11);
        }

        input.value = formatted;
    }
});

async function submitForm(event) {
    event.preventDefault();

    const form = event.target;
    const phoneInput = form.querySelector("#phone");
    const messageDiv = document.getElementById("formMessage");
    const submitButton = form.querySelector('button[type="submit"]');
    const privacyCheckbox = form.querySelector("#privacy");

    const phoneDigits = phoneInput.value.replace(/\D/g, "");
    if (phoneDigits.length !== 11) {
        messageDiv.textContent = "Введите полный номер телефона";
        messageDiv.className = "text-sm text-red-500";
        messageDiv.classList.remove("hidden");
        return;
    }

    if (!privacyCheckbox.checked) {
        messageDiv.textContent = "Необходимо согласиться с условиями обработки персональных данных";
        messageDiv.className = "text-sm text-red-500";
        messageDiv.classList.remove("hidden");
        return;
    }

    const formData = new FormData(form);

    try {
        submitButton.disabled = true;
        messageDiv.textContent = "Отправка...";
        messageDiv.className = "text-sm text-white";
        messageDiv.classList.remove("hidden");

        const response = await fetch("/submit-application", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (result.status === "success") {
            messageDiv.textContent = result.message;
            messageDiv.className = "text-sm text-green-500";
            form.reset();
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        messageDiv.textContent = error.message || "Произошла ошибка при отправке формы";
        messageDiv.className = "text-sm text-red-500";
    } finally {
        messageDiv.classList.remove("hidden");
        submitButton.disabled = false;
    }
}
