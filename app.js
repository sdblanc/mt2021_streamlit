document.addEventListener("DOMContentLoaded", () => {
    // Set header content
    document.querySelector(".hero h1").textContent = itinerary.title;
    document.querySelector(".hero .subtitle").textContent = itinerary.subtitle;

    // Build timeline
    const timeline = document.querySelector(".timeline");
    timeline.innerHTML = "";

    itinerary.days.forEach((day, index) => {
        const card = document.createElement("div");
        card.className = "day-card";

        const header = document.createElement("div");
        header.className = "day-header";
        header.innerHTML = `<span>${day.label}${day.date ? " — " + day.date : ""}</span><span class="toggle">▼</span>`;

        const body = document.createElement("div");
        body.className = "day-body";

        day.activities.forEach(act => {
            const el = document.createElement("div");
            el.className = "activity";
            el.innerHTML = `
                ${act.time ? `<div class="activity-time">${act.time}</div>` : ""}
                <div class="activity-title">${act.title}</div>
                ${act.description ? `<div class="activity-description">${act.description}</div>` : ""}
                ${act.location ? `<div class="activity-location">${act.location}</div>` : ""}
            `;
            body.appendChild(el);
        });

        // Toggle expand/collapse
        header.addEventListener("click", () => {
            body.classList.toggle("hidden");
            header.classList.toggle("collapsed");
        });

        card.appendChild(header);
        card.appendChild(body);
        timeline.appendChild(card);
    });
});
