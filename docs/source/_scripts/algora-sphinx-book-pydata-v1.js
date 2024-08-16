// This file is processed for Algora crawling and won't be sent to the frontend
new Crawler({
  appId: 'O9A3CDDIXM', // Public
  apiKey: 'be7a2c0f077007172aa49638d22778b0', // Public
  rateLimit: 8,
  maxDepth: 10,
  startUrls: [
    'https://docs.xsolla.cloud/en/latest/',
    'https://docs.xsolla.cloud/',
  ],
  sitemaps: ['https://docs.xsolla.cloud/en/latest/sitemap.xml'],
  ignoreCanonicalTo: false,
  discoveryPatterns: ['https://docs.xsolla.cloud/**'],
  actions: [
    {
      indexName: 'xsolla-dev',
      pathsToMatch: ['https://docs.xsolla.cloud/en/latest/**'],
      recordExtractor: ({ $, helpers }) => {
        // Removing DOM elements we don't want to crawl
        const toRemove = 'footer, .hash-link';
        $(toRemove).remove();

        return helpers.docsearch({
          recordProps: {
            lvl0: {
              selectors: 'header .section-nav-title, .toc-title',
              defaultValue: 'Documentation',
            },
            lvl1: '.bd-content h1',
            lvl2: '.bd-content h2',
            lvl3: '.bd-content h3',
            lvl4: '.bd-content h4',
            content: '.bd-content p, .bd-content li',
            tags: {
              defaultValue: ['docs'],
            },
          },
          indexHeadings: true,
          aggregateContent: true,
        });
      },
    },
  ],
  initialIndexSettings: {
    'xsolla-dev': {
      attributesForFaceting: ['type', 'lang', 'language', 'version', 'tags'],
      attributesToRetrieve: [
        'hierarchy',
        'content',
        'anchor',
        'url',
        'url_without_anchor',
        'type',
      ],
      attributesToHighlight: ['hierarchy', 'hierarchy_camel', 'content'],
      attributesToSnippet: ['content:10'],
      camelCaseAttributes: ['hierarchy', 'hierarchy_radio', 'content'],
      searchableAttributes: [
        'unordered(hierarchy_radio_camel.lvl0)',
        'unordered(hierarchy_radio.lvl0)',
        'unordered(hierarchy_radio_camel.lvl1)',
        'unordered(hierarchy_radio.lvl1)',
        'unordered(hierarchy_radio_camel.lvl2)',
        'unordered(hierarchy_radio.lvl2)',
        'unordered(hierarchy_radio_camel.lvl3)',
        'unordered(hierarchy_radio.lvl3)',
        'unordered(hierarchy_radio_camel.lvl4)',
        'unordered(hierarchy_radio.lvl4)',
        'unordered(hierarchy_radio_camel.lvl5)',
        'unordered(hierarchy_radio.lvl5)',
        'unordered(hierarchy_radio_camel.lvl6)',
        'unordered(hierarchy_radio.lvl6)',
        'unordered(hierarchy_camel.lvl0)',
        'unordered(hierarchy.lvl0)',
        'unordered(hierarchy_camel.lvl1)',
        'unordered(hierarchy.lvl1)',
        'unordered(hierarchy_camel.lvl2)',
        'unordered(hierarchy.lvl2)',
        'unordered(hierarchy_camel.lvl3)',
        'unordered(hierarchy.lvl3)',
        'unordered(hierarchy_camel.lvl4)',
        'unordered(hierarchy.lvl4)',
        'unordered(hierarchy_camel.lvl5)',
        'unordered(hierarchy.lvl5)',
        'unordered(hierarchy_camel.lvl6)',
        'unordered(hierarchy.lvl6)',
        'content',
      ],
      distinct: true,
      attributeForDistinct: 'url',
      customRanking: [
        'desc(weight.pageRank)',
        'desc(weight.level)',
        'asc(weight.position)',
      ],
      ranking: [
        'words',
        'filters',
        'typo',
        'attribute',
        'proximity',
        'exact',
        'custom',
      ],
      highlightPreTag: '<span class="algolia-docsearch-suggestion--highlight">',
      highlightPostTag: '</span>',
      minWordSizefor1Typo: 3,
      minWordSizefor2Typos: 7,
      allowTyposOnNumericTokens: false,
      minProximity: 1,
      ignorePlurals: true,
      advancedSyntax: true,
      attributeCriteriaComputedByMinProximity: true,
      removeWordsIfNoResults: 'allOptional',
    },
  },
});
