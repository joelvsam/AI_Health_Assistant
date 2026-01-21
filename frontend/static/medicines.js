document.addEventListener("DOMContentLoaded", function () {
    const medicineForm = document.getElementById("medicine-form");
    const medicinesTable = document.getElementById("medicines-table").getElementsByTagName("tbody")[0];
    const token = localStorage.getItem("accessToken");

    if (!token) {
        window.location.href = "patient_signin.html";
        return;
    }

    medicineForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const name = document.getElementById("medicine-name").value;
        const dosage = document.getElementById("dosage").value;
        const time = document.getElementById("time").value;
        const frequency = document.getElementById("frequency").value;

        try {
            const response = await fetch("http://localhost:8000/medicines/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ name, dosage, time, frequency }),
            });

            if (response.ok) {
                fetchMedicines(); // Refresh the list
                medicineForm.reset(); // Clear the form
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || "Failed to add medicine"}`);
            }
        } catch (error) {
            console.error("Error adding medicine:", error);
            alert("An error occurred while adding the medicine.");
        }
    });

    async function fetchMedicines() {
        try {
            const response = await fetch("http://localhost:8000/medicines/", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const medicines = await response.json();
                medicinesTable.innerHTML = ""; // Clear existing rows
                medicines.forEach(medicine => {
                    const row = medicinesTable.insertRow();
                    row.innerHTML = `
                        <td>${medicine.name}</td>
                        <td>${medicine.dosage}</td>
                        <td>${medicine.time}</td>
                        <td>${medicine.frequency}</td>
                    `;
                });
            } else {
                console.error("Failed to fetch medicines:", await response.text());
            }
        } catch (error) {
            console.error("Error fetching medicines:", error);
        }
    }

    fetchMedicines(); // Initial fetch of medicines
});
