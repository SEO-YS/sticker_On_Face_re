
function ai_image_show(newImage) {
    if(newImage) {
        newImage.setAttribute("class", 'img');
        newImage.onload = function () {
            var maxWidth = 300; // 원하는 최대 너비 설정
            var maxHeight = 300; // 원하는 최대 높이 설정

            var width = newImage.width;
            var height = newImage.height;

            if (width > height) {
                if (width > maxWidth) {
                    height *= maxWidth / width;
                    width = maxWidth;
                }
            } else {
                if (height > maxHeight) {
                    width *= maxHeight / height;
                    height = maxHeight;
                }
            }

            newImage.style.width = width + "px";
            newImage.style.height = height + "px";
            newImage.style.visibility = "hidden"; // 버튼을 누르기 전까지 이미지를 숨김
            newImage.style.objectFit = "contain";
        };
    }
    return newImage;

}

function loadFile(input) {
    var file = input.files[0]; // 선택된 파일 가져오기

    var name = document.getElementById('fileName');
    name.textContent = file.name;

    var newImage = document.createElement("img");

    // 이미지 보여주기 1줄
    newImage = ai_image_show(newImage)
    newImage.src = URL.createObjectURL(file);

    var container = document.getElementById('image-show');
    container.appendChild(newImage);
};

var submit = document.getElementById('submitButton');
submit.onclick = showImage;     // "CHECK" 버튼 클릭 시 이미지 보여주기

function showImage() {
    var newImage = document.getElementById('image-show').lastElementChild;
    newImage.style.visibility = "visible";  // 이미지를 화면에 표시

    var saveButton = document.createElement("button");
    saveButton.setAttribute("id", "saveButton");
    // saveButton.innerHTML = '<span class="saveIcon">Save</span></a>';
    saveButton.innerHTML = "<button type='button' id='saveIcon' class='saveIcon' onclick='saveIcon()'>Save</button>";
    saveButton.onclick = function() {
    saveImage(newImage); // newImage 전달
  };  // "Save" 버튼 클릭 시 이미지 저장 기능 실행
    saveButton.classList.add('buttonStyle');



    var buttonContainer = document.createElement("div");
    buttonContainer.setAttribute("class", "buttonContainer");
    buttonContainer.appendChild(saveButton);

    var container = document.getElementById('image-upload');
    container.appendChild(buttonContainer);

    submit.onclick = null; // "CHECK" 버튼 클릭 이벤트 해제

    // 숨길 요소 숨기기
    var fileContainer = document.querySelector('.fileContainer');
    var button = document.querySelector('.button');
    fileContainer.style.display = 'none';
    button.style.display = 'none';

    document.getElementById('fileName').textContent = null;
}


function saveIcon() {
    saveButton.innerHTML = "<button type='button' id='saveIcon' class='saveIcon' onclick='saveIcon()'>Save</button>"
}


function saveImage() {
    document.querySelector("#saveIcon").addEventListener("click", function() {
    // 이미지 저장 기능 구현
    alert("저장을 완료 했습니다!");

    var file = document.getElementById('chooseFile').files[0];
    var fileName = file.name;

    var formData = new FormData();
    formData.append('image', file);

    var csrftoken = getCookie('csrftoken'); // CSRF 토큰 가져오기


    $.ajax({
    url: '/common/imageUpload/',
    type: 'POST',
    headers: {
        'X-CSRFToken': csrftoken
    },
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
        // 이미지 정보 전송이 성공적으로 완료됨
        ai_image_show()
        alert ('이미지 정보 전송 완료');
            console.log('1');
        var filepath = response.filepath;
        console.log(filepath);
        var additionalInfo = response.additional_info;

//        window.location.href = "/common/cctv/?filepath=" + encodeURIComponent(filepath);
    },
    error: function(xhr, status, error) {
        // 이미지 정보 전송이 실패한 경우
        console.error('이미지 정보 전송 실패');
    }

});
});
}

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;

}



