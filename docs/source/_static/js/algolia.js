// // [This script should be loaded deferred]
// const versionMetaTag = document.querySelector('meta[name="docsearch:version"]');
// const version = versionMetaTag ? versionMetaTag.getAttribute('content') : null;
// console.log("DocSearch version:", version);
//
// const { 
// 	docsearch_app_id,
// 	docsearch_api_key,
// 	docsearch_index_name,
// } = window.docsearchConfig;
//
// // const inputDocsearchId = 'docsearch';
// const inputDocsearchId = 'search-input';
// const hashedInputDocsearchId = '#' + inputDocsearchId;
//
// // // Create the element
// // const container = document.querySelector(".article-header-buttons");
// // let docsearchDiv = document.createElement("DIV")
// // docsearchDiv.id = inputDocsearchId;
// // container.appendChild(docsearchDiv);
//
// // Initialize Algolia DocSearch after 0.1s
// setTimeout(() => {
// 	const docSearchOpts = {
// 		appId: docsearch_app_id, // public
// 		apiKey: docsearch_api_key, // public
// 		indexName: docsearch_index_name,
// 		// inputSelector: '#search-input', // sphinx_book_theme
// 		inputSelector: hashedInputDocsearchId,
// 		debug: true // Set debug to true if you want to inspect the dropdown
// 		// searchParameters: {
// 		// 	facetFilters: [
// 		// 		'language:en',
// 		// 		'version:' + version,
// 		// 	],
// 		// },
// 		// algoliaOptions: {
// 		// 	hitsPerPage: 8, // Limit the number of search results per page
// 		// }
// 	}
// 	console.log('docSearchopts:', docSearchOpts);
// 	// docsearch(docSearchOpts);
//
// 	// Verify if Algolia loaded
// 	if (typeof docsearch === 'function') {
// 		console.log('[Algolia] Ready');
// 	} else {
// 		console.log('[Algolia] NOT ready');
// 	}
// }, 100);
