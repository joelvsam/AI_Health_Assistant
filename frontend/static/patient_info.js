document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("patientForm");
    const patientList = document.getElementById("patientList");

    if (!form || !patientList) {
        return;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const symptoms = document.getElementById("symptoms").value;

        const card = document.createElement("div");
        card.classList.add("patient-card");
        card.innerHTML = `
            <strong>Name:</strong> ${name} <br>
            <strong>Age:</strong> ${age} <br>
            <strong>Gender:</strong> ${gender} <br>
            <strong>Symptoms:</strong> ${symptoms}
        `;

        patientList.appendChild(card);
        form.reset();
    });
});
