
b = %1%
b1 = %2%

if (b = "ctrl") {
    Send, ^{%b1%}
} 
else if (b = "alt") {
    Send, !{%b1%}
} 
else if (b = "shift") {
    Send, +{%b1%}
} 
else if (b = "win") {
    Send, #{%b1%}
} 
else {
    Send, {%b%}{%b1%}
}