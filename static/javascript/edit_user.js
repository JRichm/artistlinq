const newIconIMGElement = document.getElementById('image')

const iconInput = document.getElementById('new-icon-input');
iconInput.addEventListener('change', e => { 
    const file = e.target.files[0]
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            newIconIMGElement.src = e.target.result;
            newIconIMGElement.onload = initCropper;
        }
        reader.readAsDataURL(file);
    }
})

let cropper

function initCropper() {
    cropper = new Cropper(image, {
        aspectRatio: 0,
        viewMode: 0,
    })
}

document.getElementById('cropImageBtn').addEventListener('click', e => {
    e.preventDefault() 
    var croppedImage = cropper.getCroppedCanvas().toDataURL("image/png");

    document.getElementById('output').src = croppedImage

    alert(document.getElementById('output').src)
})