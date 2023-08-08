
let cropper

const newIconIMGElement = document.getElementById('image')

const iconInput = document.getElementById('new-icon-input');
iconInput.addEventListener('change', e => { 
    const file = e.target.files[0]
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            newIconIMGElement.src = e.target.result;
            newIconIMGElement.onload = initCropper;
            document.getElementById('new-icon-container').classList.remove('hidden')
            document.getElementById('cropImageBtn').addEventListener('click', cropImage)
        }
        reader.readAsDataURL(file);
    }
})

function initCropper() {
    cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 0,
    })
}

function cropImage(e) {
    e.preventDefault() 
    var croppedImage = cropper.getCroppedCanvas().toDataURL("image/png");

    document.getElementById('output').src = croppedImage

    alert(document.getElementById('output').src)
}
