// #########################################
// _static/js/algolia.js
// [This script should be loaded deferred]
// #########################################

// On click, emulate CTRL+K to bring up search UI for both buttons
const searchButtons = document.querySelectorAll('.search-button__button');
searchButtons.forEach(button => {
	button.addEventListener('click', () => {
		console.log('[js/algolia.js] Clicked search btn');
		const event = new KeyboardEvent('keydown', {
			key: 'k',
			ctrlKey: true,
			bubbles: true // Allows the event to propagate up through the DOM
		});
		document.dispatchEvent(event);
	});
});
