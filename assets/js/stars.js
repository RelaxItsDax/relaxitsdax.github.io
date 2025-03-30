document.addEventListener("DOMContentLoaded", () => {

    const pageWidth = Math.max(document.body.scrollWidth, window.innerWidth);
    const pageHeight = Math.max(document.body.scrollHeight, window.innerHeight);
    document.documentElement.style.setProperty('--page-height', `${pageHeight}px`);

    const stars1 = document.getElementById("stars1");
    const stars2 = document.getElementById("stars2");
    const stars3 = document.getElementById("stars3");

    const initialStarCount = pageHeight / 3;

    let currentShadow = window.getComputedStyle(stars1).boxShadow;
    if (currentShadow === 'none') {
        currentShadow = '';
    }

    let shadowArray1 = [];
    for (let i = 0; i < initialStarCount; i++) {
        let x = Math.random() * pageWidth;
        let y = Math.random() * pageHeight;
        shadowArray1.push(`${x}px ${y}px #a1a19a`);
        shadowArray1.push(`${x}px ${y + pageHeight}px #a1a19a`);
    }
    stars1.style.boxShadow = shadowArray1.join(', ');

    let shadowArray2 = [];
    for (let i = 0; i < initialStarCount / 2; i++) {
        let x = Math.random() * pageWidth;
        let y = Math.random() * pageHeight;
        shadowArray2.push(`${x}px ${y}px #a1a19a`);
        shadowArray2.push(`${x}px ${y + pageHeight}px #a1a19a`);
    }
    stars2.style.boxShadow = shadowArray2.join(', ');

    let shadowArray3 = [];
    for (let i = 0; i < initialStarCount / 4; i++) {
        let x = Math.random() * pageWidth;
        let y = Math.random() * pageHeight;
        shadowArray3.push(`${x}px ${y}px #a1a19a`);
        shadowArray3.push(`${x}px ${y + pageHeight}px #a1a19a`);
    }
    stars3.style.boxShadow = shadowArray3.join(', ');
});
