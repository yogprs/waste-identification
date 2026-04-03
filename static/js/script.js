document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".sidebar-menu");
  const currentPage = window.location.pathname;

  links.forEach((link) => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
});

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file-input");
const browseBtn = document.getElementById("browse-file-btn");

// Klik "browse files" buka file picker
browseBtn.addEventListener("click", () => fileInput.click());

// cegah default behavior (biar tidak buka file di browser)
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  });
});

// efek saat drag masuk
["dragenter", "dragover"].forEach((eventName) => {
  dropArea.addEventListener(eventName, () => {
    dropArea.classList.add("dragging");
  });
});

// hapus efek saat keluar
["dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, () => {
    dropArea.classList.remove("dragging");
  });
});

// handle file drop
dropArea.addEventListener("drop", (e) => {
  const files = e.dataTransfer.files;

  if (files.length > 0) {
    uploadFile(files[0]);
  }
});

// File selected via browse
fileInput.addEventListener("change", () => {
  handleFiles(fileInput.files);
});

// fungsi upload
function uploadFile(file) {
  console.log("File diterima:", file);

  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Upload sukses:", data);
    })
    .catch((err) => {
      console.error("Error:", err);
    });
}

// Process files
function handleFiles(files) {
  if (files.length === 0) return;
  const file = files[0];
  if (!file.type.startsWith("image/")) {
    alert("Please upload an image file!");
    return;
  }
  // Kirim file ke Flask via fetch
  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.text())
    .then((data) => alert(data))
    .catch((err) => console.error(err));
}

const cameraButton = document.getElementById("camera-button");

cameraButton.addEventListener("click", () => {
  window.location.href = "/camera";
});
