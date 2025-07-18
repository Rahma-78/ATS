alert("JavaScript is running!");
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
                        console.log("Form data:", formData);
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

//resultsDiv.innerHTML = ""; // Clear previous results

const analysisResultsDiv = document.createElement("div");
analysisResultsDiv.className = "analysis-results";

// Match Percentage
const matchPercentageDiv = document.createElement("div");
matchPercentageDiv.className = "match-percentage";
const matchPercentageHeading = document.createElement("h3");
matchPercentageHeading.textContent = "Match Percentage";
const matchPercentageValue = document.createElement("p");
matchPercentageValue.textContent = `${results.match_percentage}%`;
    matchPercentageValue.style.fontSize = "3em";
    matchPercentageValue.style.fontWeight = "bold";
    matchPercentageValue.style.color = "#4CAF50";
    matchPercentageValue.style.backgroundColor = "#e8f5e9";
    matchPercentageValue.style.padding = "10px";
    matchPercentageValue.style.borderRadius = "5px";
    matchPercentageValue.style.display = "inline-block";
    matchPercentageDiv.appendChild(matchPercentageHeading);
    matchPercentageDiv.appendChild(matchPercentageValue);
analysisResultsDiv.appendChild(matchPercentageDiv);

// Strengths
const strengthsDiv = document.createElement("div");
strengthsDiv.className = "strengths";
const strengthsHeading = document.createElement("h3");
strengthsHeading.textContent = "Strengths";
const strengthsList = document.createElement("ul");
if (results.strengths && Array.isArray(results.strengths)) {
    results.strengths.forEach(strength => {
        const strengthItem = document.createElement("li");
        strengthItem.textContent = strength;
            strengthItem.style.listStyleType = "none";
            strengthItem.style.marginLeft = "0";
            strengthItem.style.paddingLeft = "0";
    });
} else {
    const noStrengthsItem = document.createElement("li");
    noStrengthsItem.textContent = "No strengths identified.";
    strengthsList.appendChild(noStrengthsItem);
}
strengthsDiv.appendChild(strengthsHeading);
strengthsDiv.appendChild(strengthsList);
analysisResultsDiv.appendChild(strengthsDiv);

// Weaknesses
const weaknessesDiv = document.createElement("div");
weaknessesDiv.className = "weaknesses";
const weaknessesHeading = document.createElement("h3");
weaknessesHeading.textContent = "Weaknesses";
const weaknessesList = document.createElement("ul");
if (results.weaknesses && Array.isArray(results.weaknesses)) {
    results.weaknesses.forEach(weakness => {
        const weaknessItem = document.createElement("li");
        weaknessItem.textContent = weakness;
            weaknessItem.style.listStyleType = "none";
            weaknessItem.style.marginLeft = "0";
            weaknessItem.style.paddingLeft = "0";
    });
} else {
    const noWeaknessesItem = document.createElement("li");
    noWeaknessesItem.textContent = "No weaknesses identified.";
    weaknessesList.appendChild(noWeaknessesItem);
}
weaknessesDiv.appendChild(weaknessesHeading);
weaknessesDiv.appendChild(weaknessesList);
analysisResultsDiv.appendChild(weaknessesDiv);

// Candidate Summary
const candidateSummaryDiv = document.createElement("div");
candidateSummaryDiv.className = "candidate-summary";
const candidateSummaryHeading = document.createElement("h3");
candidateSummaryHeading.textContent = "Candidate Summary";
const candidateSummaryText = document.createElement("p");
candidateSummaryText.textContent = results.candidate_summary;
    candidateSummaryText.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.1)";
candidateSummaryDiv.appendChild(candidateSummaryHeading);
candidateSummaryDiv.appendChild(candidateSummaryText);
analysisResultsDiv.appendChild(candidateSummaryDiv);

// Recommendations
const recommendationsDiv = document.createElement("div");
recommendationsDiv.className = "recommendations";
const recommendationsHeading = document.createElement("h3");
recommendationsHeading.textContent = "Recommendations";
const recommendationsText = document.createElement("p");
recommendationsText.textContent = results.recommendations;
    recommendationsText.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.1)";
recommendationsDiv.appendChild(recommendationsHeading);
recommendationsDiv.appendChild(recommendationsText);
analysisResultsDiv.appendChild(recommendationsDiv);

// Append the analysis results to the results div
resultsDiv.appendChild(analysisResultsDiv);
        } catch (error) {
            console.error("Error analyzing resume:", error);
            resultsDiv.textContent = `An error occurred while analyzing the resume: ${error.message}`;
        } finally {
            newSpinner.remove();
        }
    });
});