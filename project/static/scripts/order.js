const dialog = document.getElementById("dialog");
function closeDialog() {
    dialog.close();
}
function openDialog() {
    dialog.showModal();
}

function openDialogOrAlert(empty) {
    if (empty == 'True') {
        alert('Your customer database is empty, create the customer before creating the order.');
    } else {
        openDialog();
    }
}

function submitForm(event, formElement) {
    event.preventDefault();

    const formData = new FormData(formElement);
	const formDataJsonString = JSON.stringify(Object.fromEntries(formData.entries()));
    const order = JSON.parse(formDataJsonString);
    console.log(formDataJsonString)
    console.log(order)

    fetch('/api/orders', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: formDataJsonString
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully added the order')
            location.reload();
        } else {
            return response.json();
        }
    })
    .then(data => {
        return Promise.reject(data)
    })
    .catch(error => {
        console.error(error)
        alert(`Error:\n${error.message}`)
    });
}

function editOrderForm(event, formElement, orderId) {
    event.preventDefault();
    event.stopPropagation();
    console.log(0, formElement)
    const formData = new FormData(formElement);
	const formDataJsonString = JSON.stringify(Object.fromEntries(formData.entries()));
    const order = JSON.parse(formDataJsonString);
    order.id = orderId;

    console.log(0, document.querySelector(`.accordion_${orderId}`))

    fetch(`/api/orders/${orderId}`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(order)
    })
    .then(response => {
        if (response.ok) {
            const data = response.json();
            data.then(modifiedOrder => {
                alert("The order is successfully updated!")
                setTimeout(() => {
                    console.log(modifiedOrder)
                    console.log('successful')
                    console.log(1, document.querySelector(`.accordion_${orderId}`))
                    document.querySelector(`.accordion_${orderId} span`).innerText = `${modifiedOrder.customer.firstName} ${modifiedOrder.customer.lastName}`
                    const formInner = document.querySelector(`.edit-form_${orderId}`);
                    console.log(formInner)
                    const selects = formInner.querySelectorAll('select');
                    const inputs = formInner.querySelectorAll('input');
                    const textAreas = formInner.querySelectorAll('textarea');

                    selects.forEach((select) => {
                        const name = select.name; 
                        const options = select.options;
                        for (const option of options) {
                            if (option.value === modifiedOrder[name]) {
                                option.selected = true;
                                break;
                            }
                        }
                        select.disabled = true;
                    });

                    inputs.forEach((input) => {
                        const name = input.name; 
                        input.value = modifiedOrder[name];
                        input.disabled = true;
                    });

                    textAreas.forEach((textarea) => {
                        textarea.value = modifiedOrder.comment;
                        textarea.disabled = true;
                    });

                    const buttons = document.querySelector(`.buttons_${orderId}`).querySelectorAll('button');
                    buttons.forEach(button => {
                        if (button.classList.contains('hide')) {
                            button.classList.replace('hide', 'show');
                        } else if (button.classList.contains('show')) {
                            button.classList.replace('show', 'hide');
                        }
                    });
                }, 600);
            })
        } else {
            return response.json();
        }
    })
    .then(data => {
        return Promise.reject(data)
    })
    .catch(error => {
        alert(`Unable to update the order due to: ${error.message}`);
    });
}

function deleteOrder(event, orderId) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/api/orders/${orderId}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully deleted the order')
            location.reload();
        } else {
            return response.json();
        }
    })
    .then(data => {
        return Promise.reject(data)
    })
    .catch(error => {
        console.error(error)
        alert(`Error:\n${error.message}`)
    });
}

function enableEdit(event, orderId) {
    event.preventDefault();
    event.stopPropagation();
    const formInner = document.querySelector(`.edit-form_${orderId}`);
    const selects = formInner.querySelectorAll('select');
    const inputs = formInner.querySelectorAll('input');
    const textAreas = formInner.querySelectorAll('textarea');
    
    selects.forEach(select => {
        select.disabled = false;
    });
    inputs.forEach(input => {
        input.disabled = false;
    });
    textAreas.forEach(textarea => {
        textarea.disabled = false;

    });
    const buttons = formInner.parentElement.querySelector('.buttons').querySelectorAll('button');
    buttons.forEach(button => {
        if (button.classList.contains('hide')) {
            button.classList.replace('hide', 'show')
        } else if (button.classList.contains('show')) {
            button.classList.replace('show', 'hide')
        }
    });
}

document.addEventListener("DOMContentLoaded", (event) => {
    const openDialogBtn = document.getElementById("openDialogBtn")
            
    openDialogBtn.addEventListener("click", () => {
        openDialogOrAlert(openDialogBtn.getAttribute('data-orders'))
    });

    const acc = document.getElementsByClassName("accordion");
    let i;

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
          this.classList.toggle("active");
          var panel = this.nextElementSibling;
          if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
          } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
          } 
        });
    }
});