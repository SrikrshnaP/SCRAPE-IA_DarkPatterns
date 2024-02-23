/**
 * The object to access the API functions of the browser.
 * @constant
 * @type {{runtime: object, i18n: object}} BrowserAPI
 */
const brw = chrome;

/**
 * Configuration of the pattern detection functions.
 * The following attributes must be specified for each pattern.
 *  - `name`: The name of the pattern that will be displayed on the UI.
 *  - `className`: A valid CSS class name for the pattern (used only internally and not displayed).
 *  - `detectionFunctions`: An array of functions `f(node, nodeOld)` to detect the pattern.
 *      Parameters of the functions are the HTML node to be examined in current and previous state (in this order).
 *      The functions must return `true` if the pattern was detected and `false` if not.
 *  - `infoUrl`: The URL to the explanation of the pattern on the `dapde.de` website.
 *  - `info`: A brief explanation of the pattern.
 *  - `languages`: An array of ISO 639-1 codes of the languages supported by the detection functions..
 * @constant
 * @type {{
 *  patterns: Array.<{
 *      name: string,
 *      className: string,
 *      detectionFunctions: Array.<Function>,
 *      infoUrl: string,
 *      info: string,
 *      languages: Array.<string>
 *  }>
 * }}
 */
export const patternConfig = {
  patterns: [
    {
      /**
       * Countdown Pattern.
       * Countdown patterns induce (truthfully or falsely) the impression that a product or service is only available for a certain period of time.
       * This is illustrated through a running clock or a lapsing bar.
       * You can watch as the desired good slips away.
       */
      name: brw.i18n.getMessage("patternCountdown_name"),
      className: "countdown",
      detectionFunctions: [
        function (node, nodeOld) {
          console.log(node.innerText);
          const reg =
            /(\d{1,2}h\s*:\s*\d{1,2}m\s*:\s*\d{1,2}s|\d{1,2}\s*hrs?\s*\d{1,2}\s*mins?|if ordered before \d{1,2}:\d{1,2}\s*(AM|PM))/i;
          if (reg.test(node.innerText)) {
            return true;
          }
          //console.log(node.innerText);
          return false;
        },
      ],
      infoUrl: brw.i18n.getMessage("patternCountdown_infoUrl"),
      info: brw.i18n.getMessage("patternCountdown_info"),
      languages: ["en", "de"],
    },
    {
      /**
       * Scarcity Pattern.
       * The Scarcity Pattern induces (truthfully or falsely) the impression that goods or services are only available in limited numbers.
       * The pattern suggests: Buy quickly, otherwise the beautiful product will be gone!
       * Scarcity Patterns are also used in versions where the alleged scarcity is simply invented or
       * where it is not made clear whether the limited availability relates to the product as a whole or only to the contingent of the portal visited.
       */
      name: brw.i18n.getMessage("patternScarcity_name"),
      className: "scarcity",
      detectionFunctions: [
        function (node, nodeOld) {
          // Return true if a match is found in the current text of the element,
          // using a regular expression for the scarcity pattern with English words.
          // The regular expression checks whether a number is followed by one of several keywords
          // or alternatively if the word group 'last/final article/item' is present.
          // The previous state of the element is not used.
          // Example: "10 pieces available"
          //          "99% claimed"
          return /\b(?:limited\s*deal|only\s*few\s*left|limited\s*items\s*in\s*stock|only\s*\d+\s*(?:items|rooms|tickets)\s*(?:available|left))\b/i.test(
            node.innerText
          );
        },
        function (node, nodeOld) {
          // Return true if a match is found in the current text of the element,
          // using a regular expression for the scarcity pattern with German words.
          // The regular expression checks whether a number is followed by one of several keywords
          // or alternatively if the word group 'last article' (`letzter\s*Artikel`) is present.
          // The previous state of the element is not used.
          // Example: "10 Stück verfügbar"
          //          "99% eingelöst"
          return /\d+\s*(?:\%|stücke?|stk\.?)?\s*(?:verfügbar|verkauft|eingelöst)|letzter\s*Artikel/i.test(
            node.innerText
          );
        },
      ],
      infoUrl: brw.i18n.getMessage("patternScarcity_infoUrl"),
      info: brw.i18n.getMessage("patternScarcity_info"),
      languages: ["en", "de"],
    },
    {
      /**
       * Social Proof Pattern.
       * Social Proof is another Dark Pattern of this category.
       * Positive product reviews or activity reports from other users are displayed directly.
       * Often, these reviews or reports are simply made up.
       * But authentic reviews or reports also influence the purchase decision through smart selection and placement.
       */
      name: brw.i18n.getMessage("patternSocialProof_name"),
      className: "social-proof",
      detectionFunctions: [
        function (node, nodeOld) {
          // Return true if a match is found in the current text of the element,
          // using a regular expression for the social proof pattern with English words.
          // The regular expression checks whether a number is followed by a combination of different keywords.
          // The previous state of the element is not used.
          // Example: "5 other customers also bought this article"
          //          "6 buyers have rated the following products [with 5 stars]"
          return /\b(?:\d+% positive ratings from \d{1,3}K\+ customers|\d{1,3}K\+ bought in past month|frequently bought together|You might be interested in)\b/i.test(
            node.innerText
          );
        },
        function (node, nodeOld) {
          // Return true if a match is found in the current text of the element,
          // using a regular expression for the social proof pattern with German words.
          // The regular expression checks whether a number is followed by a combination of different keywords.
          // The previous state of the element is not used.
          // Example: "5 andere Kunden kauften auch diesen Artikel"
          //          "6 Käufer*innen haben folgende Produkte [mit 5 Sternen bewertet]"
          return /\d+\s*(?:andere)?\s*(?:Kunden?|Käufer|Besteller|Nutzer|Leute|Person(?:en)?)(?:(?:\s*\/\s*)?[_\-\*]?innen)?\s*(?:(?:kauften|bestellten|haben)\s*(?:auch|ebenfalls)?|(?:bewerteten|rezensierten))\s*(?:diese[ns]?|(?:den|die|das)?\s*folgenden?)\s*(?:Produkte?|Artikel)/i.test(
            node.innerText
          );
        },
      ],
      infoUrl: brw.i18n.getMessage("patternSocialProof_infoUrl"),
      info: brw.i18n.getMessage("patternSocialProof_info"),
      languages: ["en", "de"],
    },
  ],
};

/**
 * Checks if the `patternConfig` is valid.
 * @returns {boolean} `true` if the `patternConfig` is valid, `false` otherwise.
 */
function validatePatternConfig() {
  // Create an array with the names of the configured patterns.
  let names = patternConfig.patterns.map((p) => p.name);
  // Check if there are duplicate names.
  if (new Set(names).size !== names.length) {
    // If there are duplicate names, the configuration is invalid.
    return false;
  }
  // Check every single configured pattern for validity.
  for (let pattern of patternConfig.patterns) {
    // Ensure that the name is a non-empty string.
    if (!pattern.name || typeof pattern.name !== "string") {
      return false;
    }
    // Ensure that the class name is a non-empty string.
    if (!pattern.className || typeof pattern.className !== "string") {
      return false;
    }
    // Ensure that the detection functions are a non-empty array.
    if (
      !Array.isArray(pattern.detectionFunctions) ||
      pattern.detectionFunctions.length <= 0
    ) {
      return false;
    }
    // Check every single configured detection function for validity.
    for (let detectionFunc of pattern.detectionFunctions) {
      // Ensure that the detection function is a function with two arguments.
      if (typeof detectionFunc !== "function" || detectionFunc.length !== 2) {
        return false;
      }
    }
    // Ensure that the info URL is a non-empty string.
    if (!pattern.infoUrl || typeof pattern.infoUrl !== "string") {
      return false;
    }
    // Ensure that the info/explanation is a non-empty string.
    if (!pattern.info || typeof pattern.info !== "string") {
      return false;
    }
    // Ensure that the languages are a non-empty array.
    if (!Array.isArray(pattern.languages) || pattern.languages.length <= 0) {
      return false;
    }
    // Check every single language for being a non-empty string.
    for (let language of pattern.languages) {
      // Ensure that the language is a non-empty string.
      if (!language || typeof language !== "string") {
        return false;
      }
    }
  }
  // If all checks have been passed successfully, the configuration is valid and `true` is returned.
  return true;
}

/**
 * @type {boolean} `true` if the `patternConfig` is valid, `false` otherwise.
 */
export const patternConfigIsValid = validatePatternConfig();

/**
 * Prefix for all CSS classes that are added to elements on websites by the extension.
 * @constant
 */
export const extensionClassPrefix = "__ph__";

/**
 * The class that is added to elements detected as patterns.
 * Elements with this class get a black border from the CSS styles.
 * @constant
 */
export const patternDetectedClassName =
  extensionClassPrefix + "pattern-detected";

/**
 * A class for the elements created as shadows for pattern elements
 * for displaying individual elements using the popup.
 */
export const currentPatternClassName = extensionClassPrefix + "current-pattern";

/**
 * A list of HTML tags that should be ignored during pattern detection.
 * The elements with these tags are removed from the DOM copy.
 */
export const tagBlacklist = ["script", "style", "noscript", "audio", "video"];
