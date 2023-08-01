let fileInput = document.getElementById('new-icon-input')
let uploadedIMG = document.getElementById('uploaded-icon');
let iconContainer = document.getElementById('new-icon-box');
let dragging = false;
let containerSize = [iconContainer.offsetWidth, iconContainer.offsetHeight];
let clickPos = [0, 0];
let diff = [0, 0];
let imageSize = [0, 0];

// when user uploads picture file
fileInput.addEventListener('change', e => {
    let diff = [0, 0];
    let clickPos = [0, 0];
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = e => {
            uploadedIMG.src = e.target.result;
            imageSize = [uploadedIMG.offsetWidth, uploadedIMG.offsetHeight] // add this to the input event listener
                                                                    // only need to get the size once each time
        }

        reader.readAsDataURL(fileInput.files[0]);
    }
    
})

// when user clicks picture
uploadedIMG.addEventListener('mousedown', e => {
    clickPos = [e.clientX - diff[0], e.clientY - diff[1]]
    dragging = true
    imageSize = [uploadedIMG.offsetWidth, uploadedIMG.offsetHeight] // add this to the input event listener
                                                                    // only need to get the size once each time the user uploads
})

// when user drags picture
window.addEventListener('mousemove', e => {
    if (dragging) {
        mousePos = [e.clientX, e.clientY]
        diff = [mousePos[0] - clickPos[0], mousePos[1] - clickPos[1]]

        if (diff[0] > 0) diff[0] = 0
        if (diff[1] > 0) diff[1] = 0
        if (diff[0] < -imageSize[0] + containerSize[0]) diff[0] = -imageSize[0] + containerSize[0]
        if (diff[1] < -imageSize[1] + containerSize[1]) diff[1] = -imageSize[1] + containerSize[1]

        uploadedIMG.style = `transform: translateX(${diff[0]}px) translateY(${diff[1]}px);`
    }
})

// when user releases click 
document.addEventListener('mouseup', e => {
    dragging = false;
})