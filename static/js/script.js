
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-upload");
    const fileLabel = document.querySelector(".form-file");
    
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
                fileLabel.classList.add("form-file-selected");
                fileLabel.innerHTML = `<i class="fas fa-file"></i> ${fileInput.files[0].name}`;
            } else {
                fileLabel.classList.remove("form-file-selected");
                fileLabel.innerHTML = `<i class="fas fa-cloud-upload-alt"></i> <span>Arrastra y suelta tu documento aquí o haz clic para seleccionarlo</span>`;
            }
        });
    });
