uploadedIMG = document.getElementById('uploaded-icon');
let dragging = false;


uploadedIMG.addEventListener('mousedown', e => {
    console.log('onmousedown')
})
document.addEventListener('mouseup', e => {
    console.log('Not dragging')
    dragging = false;
})