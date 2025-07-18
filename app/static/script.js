document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const resultsContainer = document.getElementById("results-container");
    const resultsDiv = document.getElementById("results");
    const spinner = document.createElement("div");
    spinner.className = "spinner";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        console.log("Form data:", formData);
        resultsContainer.classList.add("hidden");
        resultsDiv.innerHTML = "";
        const newSpinner = document.createElement("div");
        newSpinner.className = "spinner";
        resultsDiv.appendChild(newSpinner);
        resultsContainer.classList.remove("hidden");

        try {
            console.log("Sending request to /api/v1/analyze");
            const response = await fetch("/api/v1/analyze/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                const errorMessage = errorData?.detail || `HTTP error! status: ${response.status}`;
                throw new Error(errorMessage);
            }
console.log("Received response:", response);
const results = await response.json();
console.log("Parsed results:", results);
//resultsDiv.textContent = JSON.stringify(results, null, 2);

resultsDiv.innerHTML = ""; // Clear previous results

const heading = document.createElement("h1");
heading.textContent = "Hello, world!";
resultsDiv.appendChild(heading);
        } catch (error) {
            console.error("Error analyzing resume:", error);
            resultsDiv.textContent = `An error occurred while analyzing the resume: ${error.message}`;
        } finally {
            newSpinner.remove();
        }
    });
});