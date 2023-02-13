// Get the original blog post text
var originalText = document.getElementById("blog-post").innerHTML;

// Get the selected language
var selectedLanguage = document.getElementById("language-select").value;

// Use your text conversion model to translate the text
var translatedText = translateText(originalText, selectedLanguage);

// Update the blog post with the translated text
document.getElementById("blog-post").innerHTML = translatedText;

// Store the selected language in local storage
localStorage.setItem("selectedLanguage", selectedLanguage);

// Get the selected language from local storage
var selectedLanguage = localStorage.getItem("selectedLanguage");

// If there is no stored language, set the default language
if (!selectedLanguage) {
  selectedLanguage = "en";
}