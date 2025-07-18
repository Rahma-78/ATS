document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const resultsContainer = document.getElementById("results-container");
    const resultsDiv = document.getElementById("results");
    const spinner = document.createElement("div");
    spinner.className = "spinner";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        resultsContainer.classList.add("hidden");
        resultsDiv.innerHTML = "";
        resultsDiv.appendChild(spinner);
        resultsContainer.classList.remove("hidden");

        try {
            const response = await fetch("api/v1/analyze", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                const errorMessage = errorData?.detail || `HTTP error! status: ${response.status}`;
                throw new Error(errorMessage);
            }

            const results = await response.json();
            resultsDiv.textContent = JSON.stringify(results, null, 2);

        } catch (error) {
            console.error("Error analyzing resume:", error);
            resultsDiv.textContent = `An error occurred while analyzing the resume: ${error.message}`;
        } finally {
            spinner.remove();
        }
    });
});