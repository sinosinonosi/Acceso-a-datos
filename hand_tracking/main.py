import cv2
import time
import numpy as np
from HandTrackingModule import HandDetector
from VolumeHandControl import VolumeController
from dao.mongodb_dao import MongoDBDAO
from models.session import Session
from models.volume_event import VolumeEvent

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.7, maxHands=1)
    vol_ctrl = VolumeController()
    
    db = MongoDBDAO()
    db_status = "DB: OK" if db.connected else "DB: --"
    
    current_session = Session()
    session_id = None
    if db.connected:
        session_id = db.insert_session(current_session.to_dict())

    volBar = 400
    volPer = vol_ctrl.get_current_volume_percentage()
    last_vol_per = volPer 
    pTime = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            pinky_tip_y = lmList[20][2]
            pinky_base_y = lmList[18][2]
            is_pinky_down = pinky_tip_y > pinky_base_y
            
            length, img, lineInfo = detector.findDistance(4, 8, img)
            
            if is_pinky_down:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                volPer = vol_ctrl.set_volume(length, min_dist=20, max_dist=180)
                
                if db.connected and abs(volPer - last_vol_per) > 2:
                    event = VolumeEvent(last_vol_per, volPer, length)
                    db.insert_volume_event(event.to_dict(), session_id)
                    last_vol_per = volPer
            else:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 0, 255), cv2.FILLED)

            volBar = np.interp(length, [20, 180], [400, 150])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime > 0 else 0
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        
        color_db = (0, 255, 0) if db.connected else (0, 0, 255)
        cv2.putText(img, db_status, (40, 90), cv2.FONT_HERSHEY_COMPLEX, 1, color_db, 3)

        cv2.imshow("Control de Volumen", img)
        
        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if db.connected and session_id:
        current_session.end_session()
        db.update_session(session_id, current_session.to_dict())

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()