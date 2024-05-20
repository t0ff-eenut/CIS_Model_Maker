import cv2, csv, os, time
from picamera2 import Picamera2

g_b_RAW_CAM = True
g_i_capture_cycle = 200

g_i_A_RAW_1_CIS = [8, 100000, 2]        # 1Frame
g_i_A_RAW_12_CIS = [8, 100000, 17]      # 12Frame IDLE_MODE
g_i_A_LOW_3_CIS = [22, 100000, 6]       # 3Frame
g_i_A_LOW_12_CIS = [22, 100000, 17]     # 12Frame
g_i_A_High_12_CIS = [3, 100000, 17]     # 12Frame

if __name__ == '__main__':
    ## CSV 출력 설정 #############################
    g_s_A_csv_header = [[]]
    tmp = ["Capture Number"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["Time"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["CIS Setting"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["Gain"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["Inttime"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["Frame Rate"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["LUX"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["Capture Name"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["frame_rate_Most_Fast"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["frame_rate_Most_Slow"]
    g_s_A_csv_header[0].extend(tmp)
    tmp = ["frame_rate_Most_AVG"]
    g_s_A_csv_header[0].extend(tmp)

    print(g_s_A_csv_header)
    
    cv2.startWindowThread()
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", 1024, 1024)
    cv2.moveWindow("Frame", 0, 0)
    
    # Capture 종류 설정
    s_background_image = "Background"
    s_inter_move_image = "InterMove"
    s_occupancy_image = "Occupancy"
    print("1. " + s_background_image)
    print("2. " + s_inter_move_image)
    print("3. " + s_occupancy_image)
    s_Select = input("Captuer Name: ")
    if s_Select == "1" :
        s_folder_name = s_background_image
    elif s_Select == "2" :
        s_folder_name = s_inter_move_image
    elif s_Select == "3" :
        s_folder_name = s_occupancy_image
    s_folder_addr = s_folder_name + '/RAW_Original'
    
    # 카메라 ON
    s_RAW_1F_Set = "RAW_1F"
    s_RAW_12F_Set = "RAW_12F"
    s_LOW_3F_Set = "LOW_3F"
    s_LOW_12F_Set = "LOW_12F"
    s_HIGH_12F_Set = "HIGH_12F"
    print("1. " + s_RAW_1F_Set)
    print("2. " + s_RAW_12F_Set)
    print("3. " + s_LOW_3F_Set)
    print("4. " + s_LOW_12F_Set)
    print("5. " + s_HIGH_12F_Set)
    s_input_Select = input("CIS Setting : ")
    if s_input_Select == "1" :
        g_i_gain = g_i_A_RAW_1_CIS[0]
        g_i_inttime = g_i_A_RAW_1_CIS[1]
        g_i_Frame = g_i_A_RAW_1_CIS[2]
        s_cis_set = s_RAW_1F_Set
    elif s_input_Select == "2" :
        g_i_gain = g_i_A_RAW_12_CIS[0]
        g_i_inttime = g_i_A_RAW_12_CIS[1]
        g_i_Frame = g_i_A_RAW_12_CIS[2]
        s_cis_set = s_RAW_12F_Set
    elif s_input_Select == "3" :
        g_i_gain = g_i_A_LOW_3_CIS[0]
        g_i_inttime = g_i_A_LOW_3_CIS[1]
        g_i_Frame = g_i_A_LOW_3_CIS[2]
        s_cis_set = s_LOW_3F_Set
    elif s_input_Select == "4" :
        g_i_gain = g_i_A_LOW_12_CIS[0]
        g_i_inttime = g_i_A_LOW_12_CIS[1]
        g_i_Frame = g_i_A_LOW_12_CIS[2]
        s_cis_set = s_LOW_12F_Set
    elif s_input_Select == "5" :
        g_i_gain = g_i_A_High_12_CIS[0]
        g_i_inttime = g_i_A_High_12_CIS[1]
        g_i_Frame = g_i_A_High_12_CIS[2]
        s_cis_set = s_HIGH_12F_Set
    s_lux_input = input("LUX : ")
        
    s_folder_addr = s_folder_addr + '/' + s_cis_set
    t_now = time.localtime()
    s_now = time.strftime('%y%m%d_%H%M%S', t_now)
    s_folder_addr = s_folder_addr + '/' + s_now + '_L' + s_lux_input
    os.makedirs(s_folder_addr, exist_ok = True)
    
    g_Picamera2_PICAM_RAW = Picamera2()
    if g_b_RAW_CAM:
        g_Sensor_mode = 2 # CIS MODE 설정
        preview_config = g_Picamera2_PICAM_RAW.create_preview_configuration(raw=g_Picamera2_PICAM_RAW.sensor_modes[g_Sensor_mode],buffer_count=1)
    else : 
        preview_config = g_Picamera2_PICAM_RAW.create_preview_configuration()
    g_Picamera2_PICAM_RAW.configure(preview_config)
    g_Picamera2_PICAM_RAW.controls.AnalogueGain = g_i_gain    # GAIN 설정 
    g_Picamera2_PICAM_RAW.controls.ExposureTime = g_i_inttime # INT Time 설정
    g_Picamera2_PICAM_RAW.controls.NoiseReductionMode = g_Picamera2_PICAM_RAW.controls.NoiseReductionMode.Off
    g_Picamera2_PICAM_RAW.controls.FrameRate = g_i_Frame
    g_Picamera2_PICAM_RAW.start()
    Original_x, Original_y = g_Picamera2_PICAM_RAW.sensor_modes[g_Sensor_mode]['size']
    print(Original_x, Original_y)
    
    time.sleep(5)
    
    raw_metadata = g_Picamera2_PICAM_RAW.capture_metadata()
    d_lux = int(raw_metadata['Lux']) # 실제 LUX 값
    start_program_time = time.time()
    i_capture_count = 0
    i_frame_rate_sum = 0
    i_frame_rate_avg = 0
    i_frame_rate_Most_Fast = 99
    i_frame_rate_Most_Slow = 1
    # Capture
    while i_capture_count <= g_i_capture_cycle :
        t_capture_start_time = time.time()
        if g_b_RAW_CAM:
            RAW_image = g_Picamera2_PICAM_RAW.capture_array("raw")
        else :
            RAW_image = g_Picamera2_PICAM_RAW.capture_array()
        t_capture_end_time = time.time()
        i_Capture_Speed = (t_capture_end_time - t_capture_start_time)
        i_frame_rate = int(1 / i_Capture_Speed)
        print(i_capture_count,". Capture Speed : ", i_Capture_Speed * 1000, "ms")
        print(i_capture_count,". Frame Rate : ", i_frame_rate, "FPS")
        i_frame_rate_sum += i_frame_rate
        if i_frame_rate_Most_Fast < i_frame_rate:
            i_frame_rate_Most_Fast = i_frame_rate
        if i_frame_rate_Most_Slow > i_frame_rate:
            i_frame_rate_Most_Slow = i_frame_rate
            
        ### RAW 이미지 저장
        image_viewer = cv2.resize(RAW_image, (1024, 1024))
        cv2.imshow("Frame", image_viewer)
        cv2.waitKey(1)
        cv2.imwrite(s_folder_addr+'/G'+str(g_i_gain)+'_I'+str(g_i_inttime)+'_'+str(i_capture_count)+'_L'+str(d_lux)+'_F'+str(i_frame_rate)+'.pgm', RAW_image)
        
        # CSV 저장        
        insert_data = []
        temp = [i_capture_count]
        insert_data.extend(temp)
        temp = [s_now]
        insert_data.extend(temp)
        temp = [s_cis_set]
        insert_data.extend(temp)
        temp = [g_i_gain]
        insert_data.extend(temp)
        temp = [g_i_inttime]
        insert_data.extend(temp)
        temp = [i_frame_rate]
        insert_data.extend(temp)
        temp = [d_lux]
        insert_data.extend(temp)
        temp = [s_folder_name]
        csv_data = []
        csv_data.append(insert_data) # Data 합치기
            
        file_name = 'TP_Data'
        # 파일이 있다면
        if os.path.isfile(s_folder_addr+'/'+file_name+'.csv'):
            with open(s_folder_addr+'/'+file_name+'.csv', 'a', newline = '') as file:
                sel_file = csv.writer(file, delimiter = ',')
                sel_file.writerows(csv_data)
                print('save')
        # 파일이 없다면
        else:
            with open(s_folder_addr+'/'+file_name+'.csv', 'a', newline = '') as file:
                sel_file = csv.writer(file)
                sel_file.writerows(g_s_A_csv_header)
                sel_file = csv.writer(file, delimiter = ',')
                sel_file.writerows(csv_data)
                print('save_new')
        i_capture_count += 1
    
    insert_data = []
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = ['']
    insert_data.extend(temp)
    temp = [i_frame_rate_Most_Fast]
    insert_data.extend(temp)
    temp = [i_frame_rate_Most_Slow]
    insert_data.extend(temp)
    temp = [i_frame_rate_avg]
    csv_data = []
    csv_data.append(insert_data) # Data 합치기   
    with open(s_folder_addr+'/'+file_name+'.csv', 'a', newline = '') as file:
        sel_file = csv.writer(file, delimiter = ',')
        sel_file.writerows(csv_data)
        print('save')
    i_frame_rate_avg = int(i_frame_rate_sum / g_i_capture_cycle)
    print("Fast FrameRate : ", i_frame_rate_Most_Fast,"FPS")
    print("Slow FrameRate : ", i_frame_rate_Most_Slow,"FPS")
    print("avg FrameRate : ", i_frame_rate_avg,"FPS")


