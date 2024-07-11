function updateOrders() {
    fetch('/api/orders/check_confirmations')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#orders tbody');
            tableBody.innerHTML = '';

            data.forEach(order => {
                const row = document.createElement('tr');

                // Determine the row class based on order status
                if (order.canceled) {
                    row.className = 'canceled';
                } else if (order.confirmations >= 5) {
                    row.className = 'confirmed';
                } else if (order.confirmations > 0) {
                    row.className = 'processing';
                } else {
                    row.className = ''; // No class for 0 confirmations
                }

                // Determine the status message
                let statusMessage;
                if (order.canceled) {
                    statusMessage = 'Canceled';
                } else if (order.confirmations >= 5) {
                    statusMessage = 'Confirmed';
                } else if (order.confirmations > 0) {
                    statusMessage = 'Processing';
                } else {
                    statusMessage = 'Awaiting Payment';
                }

                row.innerHTML = `
                    <td>${order.product_name}</td>
                    <td>${order.product_price}</td>
                    <td>${order.payment_address}</td>
                    <td style="text-align: center;">${order.confirmations}/5</td>
                    <td>${statusMessage}</td>
                    <td>
                        ${order.confirmations < 1 && !order.canceled ? `
                        <form class="cancel-order-form">
                            <input type="hidden" name="order_id" value="${order.id}">
                            <button type="submit" class="cancel-button">Cancel</button>
                        </form>
                        ` : order.confirmations >= 5 ? `
                        <button class="download-button" data-order-id="${order.id}">Download Files</button>
                        ` : ''}
                    </td>
                `;

                tableBody.appendChild(row);
            });

            // Remove previous event listeners
            document.querySelectorAll('.cancel-order-form').forEach(form => {
                form.replaceWith(form.cloneNode(true));
            });

            // Add event listeners to cancel buttons
            document.querySelectorAll('.cancel-order-form').forEach(form => {
                form.addEventListener('submit', event => {
                    event.preventDefault();
                    const formData = new FormData(event.target);
                    fetch('/cancel_order', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(Object.fromEntries(formData))
                    }).then(response => response.json()).then(data => {
                        if (data.message === "Order canceled successfully.") {
                            event.target.closest('tr').classList.add('canceled');
                            event.target.closest('tr').querySelector('td:nth-child(5)').textContent = 'Canceled';
                            event.target.closest('td').innerHTML = '';
                        }
                    }).catch(error => console.error('Error:', error));
                });
            });

            // Add event listeners to download buttons
            document.querySelectorAll('.download-button').forEach(button => {
                button.addEventListener('click', event => {
                    const orderId = event.target.getAttribute('data-order-id');
                    window.location.href = `/download/${orderId}`;
                });
            });
        }).catch(error => console.error('Error:', error));
}

setInterval(updateOrders, 10000); // Check every 10 seconds
document.addEventListener('DOMContentLoaded', updateOrders);
