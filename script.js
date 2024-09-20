async function work(){
    const fileInput = document.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
    
        fetch('http://127.0.0.1:5000/upload', { 
          method: 'POST',
          body: formData
        })
        .then(response => {
          // Handle response from server
          if (response.ok) {
            console.log('File uploaded successfully');
          } else {
            console.error('Upload failed');
          }
        })
        .catch(error => {
          console.error('Error during upload:', error);
        });
      } else {
        console.error('No file selected');
      }
}

// setInterval(function() {
//     fetch('http://127.0.0.1:5000/check_status', function(data) {
//         if (data.status === 'completed') {
//             console.log('Task completed');
//             document.getElementById("main").innerHTML += '<a href="playback.html">DOWNLOAD</a>'
//         }
//     });
// }, 1000);

