function previewImage(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('preview-img').src = e.target.result;
                document.getElementById('preview-img').style.display = 'block';
                document.getElementById('preview-icon').style.display = 'none';
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
