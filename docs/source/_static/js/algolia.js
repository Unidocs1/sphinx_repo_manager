// [This script should be loaded deferred]
const { 
	docsearch_app_id,
	docsearch_api_key,
	docsearch_index_name,
} = window.docsearchConfig;
const docsearchId = 'docsearch';
const version = document.querySelector('meta[name="docsearch:version"]');
console.log("DocSearch version:", version);

// Create the element
const container = document.querySelector(".article-header-buttons");
let docsearchDiv = document.createElement("DIV")
docsearchDiv.id = 'docsearch';
container.appendChild(docsearchDiv);

// Initialize Algolia DocSearch after 0.1s
setTimeout(() => {
	docsearch({
		appId: docsearch_app_id, // public
		apiKey: docsearch_api_key, // public
		indexName: docsearch_index_name,
		// inputSelector: '#search-input', // sphinx_book_theme
		inputSelector: '#' + docsearchId,
		debug: false, // Set debug to true if you want to inspect the dropdown
		searchParameters: {
			facetFilters: [
				'language:en',
				'version:' + version,
			],
		},
		algoliaOptions: {
			hitsPerPage: 8, // Limit the number of search results per page
		}
	});

	// Verify if Algolia loaded
	if (typeof docsearch === 'function') {
		console.log('[Algolia] Ready');
	} else {
		console.log('[Algolia] NOT ready');
	}
}, 100);
