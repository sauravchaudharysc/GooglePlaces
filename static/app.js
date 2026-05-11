const form = document.getElementById("placeForm");
const placeInput = document.getElementById("placeId");
const loader = document.getElementById("loader");
const errorBox = document.getElementById("errorBox");
const resultCard = document.getElementById("resultCard");
const displayName = document.getElementById("displayName");
const shortAddress = document.getElementById("shortAddress");
const placePhoto = document.getElementById("placePhoto");
const jsonOutput = document.getElementById("jsonOutput");
const copyBtn = document.getElementById("copyBtn");

let latestJson = {};

function setLoading(isLoading) {
    loader.classList.toggle("hidden", !isLoading);
    resultCard.classList.add("hidden");
    errorBox.classList.add("hidden");
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
    resultCard.classList.add("hidden");
}

function renderResult(data) {
    latestJson = data;

    displayName.textContent = data.displayName || "Name not available";
    shortAddress.textContent = data.shortFormattedAddress || "Address not available";

    if (data.placePhotoUrl) {
        placePhoto.src = data.placePhotoUrl;
        placePhoto.alt = data.displayName || "Place photo";
    } else {
        placePhoto.removeAttribute("src");
        placePhoto.alt = "No photo available";
    }

    jsonOutput.textContent = JSON.stringify(data, null, 4);
    resultCard.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const placeId = placeInput.value.trim();

    if (!placeId) {
        showError("Please enter a valid Place ID.");
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`/api/place/${encodeURIComponent(placeId)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail ? JSON.stringify(data.detail) : "Request failed");
        }

        renderResult(data);
    } catch (error) {
        showError(error.message || "Something went wrong.");
    } finally {
        loader.classList.add("hidden");
    }
});

copyBtn.addEventListener("click", async () => {
    await navigator.clipboard.writeText(JSON.stringify(latestJson, null, 4));
    copyBtn.textContent = "Copied!";
    setTimeout(() => {
        copyBtn.textContent = "Copy";
    }, 1200);
});
