let targetTop = 20;
let currentTop = 0;

window.addEventListener('scroll', () => {
    const sidebar = document.querySelector('.sidebar');
    const rectify = sidebar.getBoundingClientRect();

    if(window.scrollY > rectify.top) {
        sidebar.style.position = 'fixed';
        targetTop = 20;
    } else {
        sidebar.style.position = 'static';
        targetTop = 0;
    }

    function animate() {
        currentTop += (targetTop - currentTop) * .7;
        sidebar.style.top = `${currentTop}px`;

        if (Math.abs(targetTop - currentTop) > 0.5) {
            window.requestAnimationFrame(animate);
        }
    }

    window.requestAnimationFrame(animate);
});