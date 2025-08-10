alert("JavaScript is running!");
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const submitBtn = document.getElementById("submit-btn");
    const loadingSpinner = document.getElementById("loading-spinner");
    const resultsContainer = document.getElementById("results-container");
    const resultsDiv = document.getElementById("results");
    const errorContainer = document.getElementById("error-container");
    const errorMessageDiv = document.getElementById("error-message");

    const ui = {
        showLoading: () => {
            if (loadingSpinner) {
                loadingSpinner.classList.remove("hidden");
            }
            submitBtn.disabled = true;
            submitBtn.textContent = "Analyzing...";
        },
        hideLoading: () => {
            if (loadingSpinner) {
                loadingSpinner.classList.add("hidden");
            }
            submitBtn.disabled = false;
            submitBtn.textContent = "Analyze";
        },
        showResults: (results) => {
            resultsContainer.classList.remove("hidden");
            errorContainer.classList.add("hidden");
            resultsDiv.innerHTML = "";
            resultsDiv.appendChild(createResults(results));
        },
        showError: (message) => {
            errorContainer.classList.remove("hidden");
            resultsContainer.classList.add("hidden");
            errorMessageDiv.textContent = message;
        },
    };

    const api = {
        analyzeResume: async (formData) => {
            const response = await fetch("/api/v1/analyze", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                const errorMessage = errorData?.detail || `HTTP error! Status: ${response.status}`;
                throw new Error(errorMessage);
            }

            return await response.json();
        },
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        ui.showLoading();

        const formData = new FormData(form);

        try {
            const results = await api.analyzeResume(formData);
            ui.showResults(results);
        } catch (error) {
            console.error("Error analyzing resume:", error);
            ui.showError(`An error occurred: ${error.message}`);
        } finally {
            ui.hideLoading();
        }
    });

    const createResults = (results) => {
        const fragment = document.createDocumentFragment();

        fragment.appendChild(createResultCard("Candidate Summary", results.candidate_summary));
        fragment.appendChild(createResultCard("Match Percentage", `${results.match_percentage}%`, 'match-percentage'));
        fragment.appendChild(createResultCard("Strengths", createList(results.strengths || [])));
        fragment.appendChild(createResultCard("Weaknesses", createList(results.weaknesses || [])));
        fragment.appendChild(createResultCard("Recommendations", createList(results.recommendations || [])));

        return fragment;
    };

    const createResultCard = (title, content, extraClass = '') => {
        const card = document.createElement("div");
        card.className = `result-card ${extraClass}`;

        const titleEl = document.createElement("h3");
        titleEl.textContent = title;
        card.appendChild(titleEl);

        if (typeof content === 'string') {
            const contentEl = document.createElement("p");
            contentEl.textContent = content;
            card.appendChild(contentEl);
        } else {
            card.appendChild(content);
        }

        return card;
    };

    const createList = (items) => {
        const ul = document.createElement("ul");
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        });
        return ul;
    };
});
