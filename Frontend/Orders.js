// Ensure apiUrl is not redeclared
if (typeof apiUrl === "undefined") {
  apiUrl = "http://127.0.0.1:5000/api"; // Replace with your API endpoint
}

// Function to fetch and display orders
async function fetchOrders() {
  const tableBody = document
    .getElementById("ordersTable")
    .querySelector("tbody");

  try {
    const response = await fetch(`${apiUrl}/order/getorders`);
    if (!response.ok) {
      throw new Error("Failed to fetch data from the server.");
    }

    const data = await response.json();
    const orders = data.orders;

    // Clear the existing table rows
    tableBody.innerHTML = "";

    // Sort orders by ordernumber
    orders.sort((a, b) => a.ordernumber - b.ordernumber);

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
                    <button class="view-button" onclick="viewOrder(${order.ordernumber})">Edit</button>
                    <button class="delete-button" onclick="deleteOrder(${order.ordernumber})">Delete</button>
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
      const response = await fetch(`${apiUrl}/order/addorder`, {
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

async function viewOrder(ordernumber) {
  const row = document.querySelector(`tr[data-ordernumber="${ordernumber}"]`);

  // Remove existing info row if it exists
  const existingInfoRow = row.nextElementSibling;
  if (existingInfoRow && existingInfoRow.classList.contains("info-row")) {
    existingInfoRow.remove();
  }
  // Fetch order information
  const orderResponse = await fetch(
    `${apiUrl}/order/getorderbyid?ordernumber=${ordernumber}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!orderResponse.ok) {
    console.error("Failed to fetch order information.");
    return;
  }

  const orderData = await orderResponse.json();

  // Create a new row to display customer and team information
  const infoRow = document.createElement("tr");
  infoRow.classList.add("info-row");
  infoRow.innerHTML = `
    <td colspan="5">
      <div class="info-container">
        <div>
          <h3>Customer Information</h3>
          <label>First Name: <input type="text" id="customerFirstname" value="${
            orderData.customer.firstname
          }"></label><br/>
          <label>Last Name: <input type="text" id="customerLastname" value="${
            orderData.customer.lastname
          }"></label><br/>
          <label>Phone Number: <input type="text" id="customerPhonenumber" value="${
            orderData.customer.phonenumber
          }"></label><br/>
          <label>Address: <input type="text" id="customerAddress" value="${
            orderData.customer.address
          }"></label><br/>
          <label>City: <input type="text" id="customerCity" value="${
            orderData.customer.city
          }"></label><br/>
        </div>
        <div>
          <h3>Team Information</h3>
          <label>Team ID: <input type="text" id="teamId" value="${
            orderData.team.teamid
          }" disabled></label><br/>
          <label>Address: <input type="text" id="teamAddress" value="${
            orderData.team.address
          }"></label><br/>
          <label>Name: <input type="text" id="teamName" value="${
            orderData.team.name
          }"></label><br/>
          <label>City ID: <input type="text" id="teamCityId" value="${
            orderData.team.cityid
          }"></label><br/>
        </div>
      </div>
      <div>
        <h3>Order Status</h3>
        <select id="orderStatus">
          <option value="Scheduled" ${
            orderData.order.status === "Scheduled" ? "selected" : ""
          }>Scheduled</option>
          <option value="In-progress" ${
            orderData.order.status === "In-progress" ? "selected" : ""
          }>In-progress</option>
          <option value="Completed" ${
            orderData.order.status === "Completed" ? "selected" : ""
          }>Completed</option>
        </select>
      </div>
      <button class="save-button" onclick="saveOrder(${ordernumber}, 
          ${orderData.customer.customerid})">
        Save
      </button>
      <button class="close-button" onclick="closeInfoRow(this)">Cancel</button>
    </td>
  `;

  // Insert the new row after the current row
  row.parentNode.insertBefore(infoRow, row.nextSibling);
}

function closeInfoRow(button) {
  const infoRow = button.parentElement;
  infoRow.remove();
}

// Function to save the updated order, customer, and team information
async function saveOrder(ordernumber, customerid) {
  const customerFirstname = document.getElementById("customerFirstname").value;
  const customerLastname = document.getElementById("customerLastname").value;
  const customerPhonenumber = document.getElementById(
    "customerPhonenumber"
  ).value;
  const customerAddress = document.getElementById("customerAddress").value;
  const customerCity = document.getElementById("customerCity").value;

  const teamId = document.getElementById("teamId").value;
  const teamAddress = document.getElementById("teamAddress").value;
  const teamName = document.getElementById("teamName").value;
  const teamCityId = document.getElementById("teamCityId").value;

  const orderStatus = document.getElementById("orderStatus").value;

  try {
    // Update customer information
    await fetch(`${apiUrl}/customer/updatecustomer`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customerid: customerid.toString(),
        firstname: customerFirstname,
        lastname: customerLastname,
        phonenumber: customerPhonenumber,
        address: customerAddress,
        city: customerCity,
      }),
    });
    // Update team information
    await fetch(`${apiUrl}/team/updateteam`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        teamid: teamId,
        address: teamAddress,
        name: teamName,
        cityid: teamCityId,
      }),
    });

    // Update order status
    await fetch(`${apiUrl}/order/updateorder`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ordernumber,
        customerid: customerid,
        teamid: teamId,
        status: orderStatus,
      }),
    });

    // Refresh the orders list
    fetchOrders();
  } catch (error) {
    console.error("Failed to save order information.", error);
  }
}

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
      const response = await fetch(`${apiUrl}/order/updateorder`, {
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
    const response = await fetch(`${apiUrl}/order/deleteorder`, {
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
