import cv2
import mtcnn
import os

face_detector = mtcnn.MTCNN()
vc = cv2.VideoCapture('./Robbery_in_PAK.mp4')
conf_t = 0.99

try:
    if not os.path.exists('Robbery_in_PAK'):
        os.makedirs('Robbery_in_PAK')
except OSError:
    print("Error: Creating directory of ", Robbery_in_PAK)
    
current_frame = 0
while vc.isOpened():
    ret, frame = vc.read()
    # frame = cv2.resize(frame, (920,880))
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(frame_rgb)
    # print(results)
    for res in results:
        x1, y1, width, height = res['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        
        confidence = res['confidence']
        if confidence < conf_t:
            continue
        key_points = res['keypoints'].values()
        orig_frame = frame.copy()
        
        cut_face = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=1)
        ore_face = orig_frame[y1:y2, x1:x2]
        
        # cv2.putText(frame, f'conf: {confidence:.3f}', (x1, y1), cv2.FONT_ITALIC, 1, (0, 0, 255), 1)
        
        # print("111111111111111 ",key_points)
        folderName = 'Robbery_in_PAK'
        if ret:
            name = folderName+'/face-'+ str(current_frame)+ '.jpg'
            print('Creating.....'+ name)
            # cv2.imwrite(name, cut_face)
            cv2.imwrite(name, ore_face)
            current_frame += 1
        else:
            break
        # for point in key_points:
        #     cv2.circle(frame, point, 5, (0, 255, 0), thickness=-1)
            # print("111111111111111 ",point)

    cv2.imshow('friends', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break