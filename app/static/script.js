document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const resultsContainer = document.getElementById("results-container");
    const resultsDiv = document.getElementById("results");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        resultsContainer.classList.add("hidden");

        try {
            const response = await fetch("/api/v1/analyze/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            resultsDiv.textContent = JSON.stringify(results, null, 2);
            resultsContainer.classList.remove("hidden");

        } catch (error) {
            console.error("Error analyzing resume:", error);
            resultsDiv.textContent = "An error occurred while analyzing the resume. Please try again.";
            resultsContainer.classList.remove("hidden");
        }
    });
});