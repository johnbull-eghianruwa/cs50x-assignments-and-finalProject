const dialog = document.getElementById("dialog");
function closeDialog() {
    dialog.close();
}
function openDialog() {
    dialog.showModal();
}

function submitForm(event, formElement) {
    event.preventDefault();

    const formData = new FormData(formElement);
	const formDataJsonString = JSON.stringify(Object.fromEntries(formData.entries()));

    console.log(formDataJsonString)

    fetch('/api/customers', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: formDataJsonString
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully added the customer')
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

function editCustomerForm(event, formElement, customerId) {
    event.preventDefault();
    console.log(0, formElement)
    const formData = new FormData(formElement);
	const formDataJsonString = JSON.stringify(Object.fromEntries(formData.entries()));
    const customer = JSON.parse(formDataJsonString);
    customer.id = customerId;

    console.log(0, document.querySelector(`.accordion_${customerId}`))

    fetch(`/api/customers/${customerId}`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(customer)
    })
    .then(response => {
        if (response.ok) {
            const data = response.json();
            data.then(modifiedCustomer => {
                setTimeout(() => {
                    alert('Successfully modified the customer')
                    console.log(modifiedCustomer)
                    console.log('successful')
                    console.log(1, document.querySelector(`.accordion_${customerId}`))
                    document.querySelector(`.accordion_${customerId} span`).innerText = `${modifiedCustomer.firstName} ${modifiedCustomer.lastName}`
                    const formInner = document.querySelector(`.edit-form_${customerId}`);
                    console.log(formInner)
                    const inputs = formInner.querySelectorAll('input');
                    const textAreas = formInner.querySelectorAll('textarea');
        
                    inputs.forEach((input) => {
                        const name = input.name; 
                        switch (name) {
                            case 'gender':
                                input.checked = input.value === modifiedCustomer[name];
                                break;
                            default:
                                input.value = modifiedCustomer[name];
                        }
                        input.disabled = true;
                    });
        
                    textAreas.forEach((textarea) => {
                        if (textarea.name === "measurement") {
                            textarea.value = modifiedCustomer.measurement;
                        } else {
                            textarea.value = modifiedCustomer.comment;
                        }
                        textarea.disabled = true;
                    });
        
                    const buttons = document.querySelector(`.buttons_${customerId}`).querySelectorAll('button');
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
        alert(`Unable to update the customer due to: ${error.message}`);
    });
}

function deleteCustomer(event, customerId) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/api/customers/${customerId}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully deleted the customer')
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

function enableEdit(event, customerId) {
    event.preventDefault();
    event.stopPropagation();
    const formInner = document.querySelector(`.edit-form_${customerId}`);
    const inputs = formInner.querySelectorAll('input');
    const textAreas = formInner.querySelectorAll('textarea');
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
        openDialog();
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