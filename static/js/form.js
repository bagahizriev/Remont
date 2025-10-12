async function submitForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById("formMessage");
    const submitButton = form.querySelector('button[type="submit"]');

    try {
        submitButton.disabled = true;
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
