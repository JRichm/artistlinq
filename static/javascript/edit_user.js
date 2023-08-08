
let iconCropper
let newIcon
const newIconIMGElement = document.getElementById('image')

const iconInput = document.getElementById('new-icon-input');
iconInput.addEventListener('change', handleInput)

const saveChangesbutton = document.getElementById('save-changes-button');
saveChangesbutton.addEventListener('click', handleSave)

function handleInput(inputEvent) {
    newIcon = inputEvent.target.files[0]
    if (newIcon) {
        const reader = new FileReader();
        reader.onload = (readerEvent) => {
            newIconIMGElement.src = readerEvent.target.result;
            newIconIMGElement.onload = initCropper;
            document.getElementById('new-icon-container').classList.remove('hidden')
            document.getElementById('cropImageBtn').addEventListener('click', cropImage)
        }
        reader.readAsDataURL(newIcon);
    }
}

function initCropper() {
    iconCropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 0,
    })
}

function cropImage(cropButtonEvent) {
    cropButtonEvent.preventDefault() 
    var croppedImage = iconCropper.getCroppedCanvas().toDataURL("image/png");

    document.getElementById('output').src = croppedImage
}

function handleSave(saveEvent) {
    cropImage(saveEvent)

    saveEvent.preventDefault()
    let formData = new FormData();

    if (iconCropper) {
        formData.append('newIcon', newIcon)
    }

    fetch('/update_user_appearance', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url
        } else {
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
    })
    .catch(err => {
        console.log(err)
    })
}