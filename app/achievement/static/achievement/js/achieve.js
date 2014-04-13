/**
 *
 */
RegExp.escape = function(s) {
    /**
     * Escapes a string passed to it for consumption by the RegExp
     * constructor.  Reference: http://stackoverflow.com/questions/3561493/
     *
     * @param {String} s
     * @return {String}
     */
    return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
};


String.prototype.format = function () {
    /**
     * Formats a string using {i} as selectors where i is an
     * Integer.  Replaces it with the corresponding string in the
     * arguments list.
     *
     * @return {String}
     */
    var patt,
        string = this,
        replacements = Array.prototype.slice.call(arguments, 0);

    // For each replacement text, replace the appropriately index
    // item
    for (var i = 0; i < replacements.length; ++i) {
        patt = new RegExp(RegExp.escape('{' + i + '}'), 'g');
        string = string.replace(patt, replacements[i]);
    }
    return string;
};


String.prototype.template = function (keywords) {
    /**
     * Renders a template
     *
     * @param {Object} keywords
     * @return {Object}
     */
    var patt,
        string = this;

    for (var key in keywords) {
        patt = new RegExp('<%=\\s*' + key + '\\s*%>', 'gi');
        string = string.replace(patt, keywords[key]);
    }
    // Fallback for preventing injection
    string = string
        .replace("<script>", "")
        .replace("</script>", "");
    return string;
};


String.prototype.toTitleCase = function () {
    /**
     * Formats a string in titlecase.
     *
     * @return {String}
     */
    var string = this,
        peices = string.split(" ");

    for (var i = 0; i < peices.length; ++i) {
        peices[i] = peices[i][0].toUpperCase() + peices[i].substr(1);
    }

    return peices.join(" ");
};
