import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 이미지 파일
IMAGE_PATH = "face.jpg"

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Image not found.")
    exit()

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=False,
    min_detection_confidence=0.5
) as face_mesh:

    result = face_mesh.process(rgb)

    if not result.multi_face_landmarks:
        print("Face not detected.")
        exit()

    h, w, _ = image.shape

    for face_landmarks in result.multi_face_landmarks:

        # 얼굴 Mesh 연결선 출력
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0),
                thickness=1,
                circle_radius=1
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(180, 180, 0),
                thickness=1
            )
        )

        # 각 Landmark 번호 표시
        for idx, landmark in enumerate(face_landmarks.landmark):

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.putText(
                image,
                str(idx),
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.25,
                (0, 150, 0),
                1,
                cv2.LINE_AA
            )

            cv2.circle(
                image,
                (x, y),
                1,
                (0, 255, 0),
                -1
            )

# 결과 저장
cv2.imwrite("face_landmark_result.jpg", image)

# 화면 출력
cv2.imshow("MediaPipe Face Landmarks", image)
cv2.waitKey(0)
cv2.destroyAllWindows()