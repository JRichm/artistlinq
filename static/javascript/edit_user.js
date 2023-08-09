
let iconCropper
let newIcon
let sendImage
let croppedImage

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
    if (cropButtonEvent) {
        cropButtonEvent.preventDefault() 
    }
    const croppedCanvas = iconCropper.getCroppedCanvas();
    croppedImage = croppedCanvas.toDataURL("image/png");

    document.getElementById('output').src = croppedImage;

    // Convert the cropped canvas data to a Blob object
    croppedCanvas.toBlob(function (blob) {
        sendImage = new File([blob], 'cropped_icon.png');
    }, 'image/png');
}

function handleSave(saveEvent) {
    if (saveEvent) {
        saveEvent.preventDefault()
    }

    if (croppedImage) {
        let formData = new FormData();

        if (iconCropper) {
            formData.append('newIcon', sendImage)
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
    } else {
        cropImage()
        setTimeout(() => {
            handleSave()
        }, 75)
    }
    
}