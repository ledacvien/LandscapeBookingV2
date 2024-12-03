// Function to fetch and display orders
async function fetchOrders() {
  const tableBody = document
    .getElementById("ordersTable")
    .querySelector("tbody");

  try {
    const response = await fetch(`${window.apiUrl}/order/getorders`);
    if (!response.ok) {
      throw new Error("Failed to fetch data from the server.");
    }

    const data = await response.json();
    const orders = data.orders;

    // Clear the existing table rows
    tableBody.innerHTML = "";

    // Populate table rows
    orders.forEach((order) => {
      const row = document.createElement("tr");
      row.setAttribute("data-ordernumber", order.ordernumber); // Add this line

      row.innerHTML = `
                <td>${order.ordernumber}</td>
                <td>${order.customerid}</td>
                <td>${order.teamid}</td>
                <td>${order.status}</td>
                <td>
                    <button onclick="editOrder(${order.ordernumber})">Edit</button>
                    <button onclick="deleteOrder(${order.ordernumber})">Delete</button>
                </td>
            `;

      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error(error);
  }
}

// Function to add an order
document
  .getElementById("addOrderForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch(`${window.apiUrl}/order/addorder`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to add order.");
      }

      fetchOrders();
      event.target.reset();
    } catch (error) {
      console.error(error);
    }
  });

// Function to edit an order
async function editOrder(ordernumber) {
  const row = document.querySelector(`tr[data-ordernumber="${ordernumber}"]`);
  const customerCell = row.querySelector("td:nth-child(2)");
  const teamCell = row.querySelector("td:nth-child(3)");
  const statusCell = row.querySelector("td:nth-child(4)");

  const originalStatus = statusCell.textContent;

  const statusDropdown = document.createElement("select");
  statusDropdown.innerHTML = `
        <option value="Scheduled">Scheduled</option>
        <option value="In-progress">In-progress</option>
        <option value="Completed">Completed</option>
    `;
  statusDropdown.value = statusCell.textContent;
  statusCell.innerHTML = "";
  statusCell.appendChild(statusDropdown);

  const saveButton = document.createElement("button");
  saveButton.textContent = "Save";
  saveButton.onclick = async () => {
    const newStatus = statusDropdown.value;

    try {
      const response = await fetch(`${window.apiUrl}/order/updateorder`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ordernumber,
          customerid: customerCell.textContent,
          teamid: teamCell.textContent,
          status: newStatus,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to update order.");
      }

      fetchOrders();
    } catch (error) {
      console.error(error);
    }
  };

  const cancelButton = document.createElement("button");
  cancelButton.textContent = "Cancel";
  cancelButton.onclick = () => {
    statusCell.innerHTML = originalStatus;
  };

  statusCell.appendChild(saveButton);
  statusCell.appendChild(cancelButton);
}

// Function to delete an order
async function deleteOrder(ordernumber) {
  if (!confirm("Are you sure you want to delete this order?")) {
    return;
  }

  try {
    const response = await fetch(`${window.apiUrl}/order/deleteorder`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ordernumber }),
    });

    if (!response.ok) {
      throw new Error("Failed to delete order.");
    }

    fetchOrders();
  } catch (error) {
    console.error(error);
  }
}

// Fetch orders on page load
fetchOrders();
