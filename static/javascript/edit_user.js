
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let fileInput = document.getElementById('new-icon-input')
const uploadedIMG = document.getElementById('uploaded-icon');
const iconContainer = document.getElementById('new-icon-box');
let dragging = false;
let uploadedImage = null;
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
            const img = new Image()
            img.onload = e => {
                uploadedImage = img;
            }

            uploadedIMG.src = e.target.result;
        }

        reader.readAsDataURL(fileInput.files[0]);
    }
})

// when user clicks picture
uploadedIMG.addEventListener('mousedown', e => {
    imageSize = [uploadedIMG.offsetWidth, uploadedIMG.offsetHeight] // add this to the input event listener
                                                                    // only need to get the size once each time
    console.log('new click w/ diff: ', diff)
    console.log('dragging')
    clickPos = [e.clientX - diff[0], e.clientY - diff[1]]
    dragging = true
})

// when user drags picture
window.addEventListener('mousemove', e => {
    if (dragging) {
        mousePos = [e.clientX, e.clientY]
        diff = [mousePos[0] - clickPos[0], mousePos[1] - clickPos[1]]

        if (diff[0] > 0) diff[0] = 0
        if (diff[1] > 0) diff[1] = 0
        if (-diff[0] > uploadedIMG.offsetWidth - containerSize[0]) diff[0] = -uploadedIMG.offsetWidth + containerSize[0]
        if (-diff[1] > uploadedIMG.offsetHeight - containerSize[1]) diff[1] = -uploadedIMG.offsetHeight + containerSize[1]
        uploadedIMG.style = `transform: translateX(${diff[0]}px) translateY(${diff[1]}px);`
    }
})

// when user releases click 
document.addEventListener('mouseup', e => {
    console.log('new diff: ', diff)
    dragging = false;
})

// Add the saveButton event listener as you provided

saveButton = document.getElementById('fake-save');
saveButton.addEventListener('click', e => {
    e.preventDefault();

    imageSize = [uploadedIMG.offsetWidth, uploadedIMG.offsetHeight]
    ctx.drawImage(uploadedIMG, -diff[0], -diff[1], 400, 400, 0, 0, 300, 150)
});