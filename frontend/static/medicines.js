document.addEventListener("DOMContentLoaded", function () {
    const medicineForm = document.getElementById("medicine-form");
    const medicinesTable = document.getElementById("medicines-table").getElementsByTagName("tbody")[0];
    const token = localStorage.getItem("accessToken");
    const apiBase = "/api";

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
            const response = await fetch(`${apiBase}/medicines/`, {
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
            const response = await fetch(`${apiBase}/medicines/`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const medicines = await response.json();
                medicinesTable.innerHTML = ""; // Clear existing rows
                medicines.forEach(medicine => {
                    const row = medicinesTable.insertRow();
                    row.setAttribute('data-id', medicine.id); // Set the id on the row
                    row.innerHTML = `
                        <td>${medicine.name}</td>
                        <td>${medicine.dosage}</td>
                        <td>${medicine.time}</td>
                        <td>${medicine.frequency}</td>
                        <td>
                            <button class="edit-btn" data-id="${medicine.id}">Edit</button>
                            <button class="delete-btn" data-id="${medicine.id}">Delete</button>
                        </td>
                    `;
                });
            } else {
                console.error("Failed to fetch medicines:", await response.text());
            }
        } catch (error) {
            console.error("Error fetching medicines:", error);
        }
    }

    // Event delegation for edit and delete buttons
    medicinesTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
            const medicineId = e.target.getAttribute('data-id');
            deleteMedicine(medicineId);
        }
        if (e.target.classList.contains('edit-btn')) {
            const medicineId = e.target.getAttribute('data-id');
            handleEdit(medicineId);
        }
    });

    async function deleteMedicine(medicineId) {
        if (!confirm('Are you sure you want to delete this medicine?')) {
            return;
        }

        try {
            const response = await fetch(`${apiBase}/medicines/${medicineId}`, {
                method: 'DELETE',
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (response.ok) {
                fetchMedicines(); // Refresh the list
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || "Failed to delete medicine"}`);
            }
        } catch (error) {
            console.error('Error deleting medicine:', error);
            alert('An error occurred while deleting the medicine.');
        }
    }

    function handleEdit(medicineId) {
        const row = medicinesTable.querySelector(`tr[data-id='${medicineId}']`);
        const cells = row.querySelectorAll('td');

        // Toggle to edit mode
        if (row.classList.contains('editing')) {
            // Save changes
            const inputs = row.querySelectorAll('input');
            const updatedMedicine = {
                name: inputs[0].value,
                dosage: inputs[1].value,
                time: inputs[2].value,
                frequency: inputs[3].value,
            };
            updateMedicine(medicineId, updatedMedicine);
        } else {
            // Enter edit mode
            row.classList.add('editing');
            for (let i = 0; i < cells.length - 1; i++) { // Exclude actions cell
                const cell = cells[i];
                const value = cell.textContent;
                cell.innerHTML = `<input type="text" value="${value}">`;
            }
            const editButton = row.querySelector('.edit-btn');
            editButton.textContent = 'Save';
        }
    }

    async function updateMedicine(medicineId, medicineData) {
        try {
            const response = await fetch(`${apiBase}/medicines/${medicineId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify(medicineData),
            });

            if (response.ok) {
                fetchMedicines(); // Refresh the list to show updated data
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || 'Failed to update medicine'}`);
            }
        } catch (error) {
            console.error('Error updating medicine:', error);
            alert('An error occurred while updating the medicine.');
        }
    }

    fetchMedicines(); // Initial fetch of medicines
});
