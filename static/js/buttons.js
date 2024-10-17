function delete_note(titleNote){
    if (confirm(`Are you sure you want to delete the ${titleNote} Note?`))
    fetch(`/delete/${titleNote}`,{
    method: "DELETE",
    headers: {
        
    }
       
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    console.log(data);
})
.catch(error => {
    console.error('There was a problem with the delete operation:', error);
});
}


function update_note(){
    const title = document.querySelector("input[name='Title']").value;
    const note = document.querySelector("input[name='Note']").value;

    const updateNote={note};

    console.log(updateNote);

    fetch(`/update/${title}`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json' // Specify the content type as JSON
        },
        body: JSON.stringify(updateNote) // Send the updated customer object as the request body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log(data); // Log the response data
    })
    .catch(error => {
        console.error('There was a problem with the update operation:', error);
    });
}



