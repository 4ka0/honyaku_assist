// Function to show a Bootstrap spinner in the form submit button (the
// 'translate' button) and disable the button when the button is clicked.
function showSpinner() {
    const btn = document.getElementById('submit-button');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>&nbspTranslating...';
    btn.classList.add('disabled');
}

// Add an event listener to perform some actions after results have been
// retrieved from the various translation APIs.
document.body.addEventListener('htmx:afterSwap', () => {
    // Set the focus on the textarea also with the previous query selected.
    // Makes it easy for the user to either delete or revise the previous query.
    const textArea = document.getElementById('id_source_text');
    textArea.focus();
    textArea.select();
    // Reset the form submit button to its initial state.
    // I.e. remove the spinner animation and remove the disabled class.
    const submitButton = document.getElementById('submit-button');
    submitButton.innerHTML = 'Translate';
    submitButton.classList.remove('disabled');
});
