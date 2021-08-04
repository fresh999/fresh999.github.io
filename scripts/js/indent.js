// get block however you want.
var block = document.getElementById("the-code");

// remove leading and trailing white space.
var code = block.innerHTML
    .split('\n')
    .filter(l => l.trim().length > 0)
    .join('\n');

// find the first non-empty line and use its
// leading whitespace as the amount that needs to be removed
var firstNonEmptyLine = block.textContent
    .split('\n')
    .filter(l => l.trim().length > 0)[0];

// using regex get the first capture group
var leadingWhiteSpace = firstNonEmptyLine.match(/^([ ]*)/);

// if the capture group exists, then use that to
// replace all subsequent lines.
if(leadingWhiteSpace && leadingWhiteSpace[0]) {
    var whiteSpace = leadingWhiteSpace[0];
    code = code.split('\n')
        .map(l => l.replace(new RegExp('^' + whiteSpace + ''), ''))
        .join('\n');
}

// update the inner HTML with the edited code
block.innerHTML = code;

