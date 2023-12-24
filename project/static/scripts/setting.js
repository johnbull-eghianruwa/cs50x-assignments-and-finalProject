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
    const user = JSON.parse(formDataJsonString);

    if (user.password === user.confirm) {
        delete user['confirm']

        fetch('/api/users', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        })
        .then(response => {
            if (response.ok) {
                alert('Successfully added the user')
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
    } else {
        alert("Error:\nThe password does not match the re-typed password")
    } 
}

function editUserForm(event, formElement, userId, userName) {
    event.preventDefault();
    console.log(0, formElement)
    const formData = new FormData(formElement);
	const formDataJsonString = JSON.stringify(Object.fromEntries(formData.entries()));
    const user = JSON.parse(formDataJsonString);

    if (user.password === user.confirm) {
        delete user['confirm']
        user.id = userId;
        user.username = userName;

        console.log(0, document.querySelector(`.accordion_${userId}`))

        fetch(`/api/users/${userId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        })
        .then(response => {
            if (response.ok) {
                const data = response.json();
                data.then(modifiedUser => {
                    alert("The user is successfully updated!")

                    setTimeout(() => {
                        console.log(modifiedUser)
                        console.log('successful')
                        console.log(1, document.querySelector(`.accordion_${userId}`))
                        document.querySelector(`.accordion_${userId} span`).innerText = `${modifiedUser.username}`
                        const formInner = document.querySelector(`.edit-form_${userId}`);
                        console.log(formInner)
                        const inputs = formInner.querySelectorAll('input');
        
                        inputs.forEach((input) => {
                            input.value = modifiedUser['password'];
                            input.disabled = true;
                        });
        
                        const div = document.querySelector(`.confirm-password_${userId}`);
                        div.classList.replace('show', 'hide');
        
                        const buttons = document.querySelector(`.buttons_${userId}`).querySelectorAll('button');
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
            alert(`Unable to update the user due to: ${error.message}`);
        });
    } else {
        alert("Error:\nThe password does not match the re-typed password")
    }
}

function deleteUser(event, userId) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/api/users/${userId}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully deleted the user')
            location.reload();
        } else {
            return response.json();
        }
    })
    .then(data => {
        return Promise.reject(data)
    })
    .catch(error => {
        alert(`Error:\n${error.message}`)
    });
}

function enableEdit(event, userId) {
    event.preventDefault();
    event.stopPropagation();
    console.log(userId)
    const formInner = document.querySelector(`.edit-form_${userId}`);
    const inputs = formInner.querySelectorAll('input');

    const div = document.querySelector(`.confirm-password_${userId}`);
    div.classList.replace('hide', 'show');
    
    inputs.forEach(input => {
        input.disabled = false;
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

document.addEventListener("DOMContentLoaded", () => {
    const openDialogBtn = document.getElementById("openDialogBtn")
    
    if (openDialogBtn) {
        openDialogBtn.addEventListener("click", () => {
            openDialog();
        });
    }

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