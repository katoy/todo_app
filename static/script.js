const languageSelect = document.getElementById('language-select');
languageSelect.addEventListener('change', function() {
    const lang = this.value;
    window.location.href = '/?lang=' + lang;
});
