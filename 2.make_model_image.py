from genericpath import isfile
import cv2, os, csv
from queue import Queue
import numpy as np

def is_folder(s_Target_Folder_pointer):
    global count_files
    s_path = s_Target_Folder_pointer
    s_A_path = s_path.split('/')

    if not s_A_path[int(len(s_A_path))-1] == 'Process':
        for dir_member in os.listdir(s_path):                 #폴더 안에 파일 확인
            if os.path.isdir(s_path+'/'+dir_member):          #폴더가 맞으면 재귀함수
                is_folder(s_path+'/'+dir_member)
            elif (s_path+'/'+dir_member).endswith('.pgm'):    #찾는 파일이 맞을경우
                try:
                    s_file_addr = s_path+'/'+dir_member
                    q_data_addr.put(s_file_addr)
                    count_files += 1
                except:
                    pass
    else:
        print("index_PASS")
            
def illumination(i_scale, F_process_image):
    if i_scale == 0:
        i_x_size = i_y_size = 64
    elif i_scale == 1:
        i_x_size = i_y_size = 16
    # elif i_scale == 2:
    #     i_x_size = i_y_size = 8
    ##################################################### illumination #####################################################################
    i_process_illu = 0
    for index in range(i_y_size*i_x_size):
        i_process_illu += F_process_image[int(index/i_y_size), int(index%i_x_size)]
    i_process_illu /= (i_x_size * i_y_size) # 측정 조도 값
    
    return int(i_process_illu) # 측정 조도 값
    ##################################################### illumination #####################################################################

if __name__ == '__main__':
    
    cv2.startWindowThread()
    cv2.namedWindow("RAW_Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("RAW_Frame", 1024, 1024)
    cv2.moveWindow("RAW_Frame", 0, 0)
    cv2.namedWindow("64x64", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("64x64", 240, 240)
    cv2.moveWindow("64x64", 0, 1100)
    cv2.namedWindow("16x16", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("16x16", 240, 240)
    cv2.moveWindow("16x16", 360, 1100)
    # cv2.namedWindow("8x8", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("8x8", 240, 240)
    # cv2.moveWindow("8x8", 720, 1100)
    q_data_addr = Queue()
    count_files = 0
    s_Target_Folder_pointer = './'
  
    for dir_member in os.listdir(s_Target_Folder_pointer):
        if os.path.isdir(s_Target_Folder_pointer+'/'+dir_member):
            is_folder(s_Target_Folder_pointer+'/'+dir_member)

    # print("q_data_addr.qsize() : ", q_data_addr.qsize())    
    while not q_data_addr.empty():
        i_A_illuminance = [0] * 2
        # i_A_illuminance = [0] * 3
        s_file_addr = q_data_addr.get()
    
        s_A_file_addr = s_file_addr.split('/')
        s_process_file_addr = ''
        for i in range(len(s_A_file_addr)):
            if s_A_file_addr[i] == '':
                continue
            elif s_A_file_addr[i] == 'RAW_Original':
                s_process_file_addr = s_process_file_addr + 'Process/'
            elif i == len(s_A_file_addr) - 1:
                # s_process_file_addr_8 = s_process_file_addr + '8_' + s_A_file_addr[i]
                s_process_file_addr_16 = s_process_file_addr + '16_' + s_A_file_addr[i]
                s_process_file_addr_64 = s_process_file_addr + '64_' + s_A_file_addr[i]
            else:
                s_process_file_addr = s_process_file_addr + s_A_file_addr[i] + '/'
                
        if not (isfile(s_process_file_addr_16) and isfile(s_process_file_addr_64)):
            
        #if not (isfile(s_process_file_addr_8) and isfile(s_process_file_addr_16) and isfile(s_process_file_addr_64)):
            F_RAW = cv2.imread(s_file_addr, cv2.IMREAD_UNCHANGED)
            F_image_viewer = cv2.resize(F_RAW, (1024, 1024))
            cv2.imshow("RAW_Frame", F_image_viewer)
        
            if not s_A_file_addr[3] == 'Process':
                s_find_folder = s_A_file_addr[2]+'/Process/'+ s_A_file_addr[4] +'/'+ s_A_file_addr[5]
                s_split_file_process = s_A_file_addr[6].split('_')
                
                if not s_split_file_process[0].isdigit():
                    b_folder_exist = os.path.isdir(s_find_folder) # 폴더 존재
                    if not b_folder_exist:        # Process folder가 존재하지 않는다면
                        os.makedirs(s_find_folder, exist_ok = True)
                    F_picture = F_RAW
                    i_picture_y, i_picture_x = F_picture.shape        # 2028 1520 # 1520 3072 # 3040 6112
                    i_CAM_PIXEL_x = 2028
                    i_CAM_PIXEL_y = 1520
                    for j in range(i_picture_x-1, int(i_CAM_PIXEL_x*1.5)-1 ,-1):
                        F_picture = np.delete(F_picture, j, 1) 
                    A = F_picture.reshape(int(F_picture.size/3),3)
                    A  = np.delete(A, 2, 1)
                    A = A.reshape(i_CAM_PIXEL_y, i_CAM_PIXEL_x) # 1520, 2028
                    
                    i_RAW_y, i_RAW_x = A.shape
                    # 64x64 16x16 8x8 PGM, CSV
                    
                    for i_scale in range(2):                    
                    # for i_scale in range(3):
                        if i_scale == 0 and s_process_file_addr_64:
                            i_x_size = i_y_size = 64
                        elif i_scale == 1 and s_process_file_addr_16:
                            i_x_size = i_y_size = 16
                        # elif i_scale == 2 and s_process_file_addr_8:
                        #     i_x_size = i_y_size = 8
                    
                        F_temp = np.zeros((i_y_size,i_x_size), np.uint8)    # 빈 공간 생성
                        i_x_raising = int(i_RAW_x / i_x_size)                                              # x_증가 폭
                        i_x_start = int(i_x_raising / 2)                                                        # x_시작 점
                        i_y_raising = int(i_RAW_y / i_y_size)                                              # y_증가 폭
                        i_y_start = int(i_y_raising / 2)                                                        # y_시작 점
                        for point in range(0, i_y_size * i_x_size, 1):                                      # 모든 픽셀에 대해서            
                            F_temp[int(point / i_x_size), int(point % i_x_size)] = A[i_y_start + (i_y_raising * int(point / i_x_size)), i_x_start + (i_x_raising * int(point % i_x_size))] ## 8x8 에서 위치에 해당하는 Pixel을 추출
                        F_process_image = F_temp
                        
                        if i_scale == 0 and s_process_file_addr_64:
                            cv2.imshow("64x64", F_process_image)
                            s_process_image_name = s_find_folder + '/64_' + s_A_file_addr[6]
                        elif i_scale == 1 and s_process_file_addr_16:
                            cv2.imshow("16x16", F_process_image)
                            s_process_image_name = s_find_folder + '/16_' + s_A_file_addr[6]
                        # elif i_scale == 2 and s_process_file_addr_8:
                        #     cv2.imshow("8x8", F_process_image)
                        #     s_process_image_name = s_find_folder + '/8_' + s_A_file_addr[6]
                        cv2.waitKey(1)
                        cv2.imwrite(s_process_image_name, F_process_image)
                    
                        ## 벡터 값으로 출력하기
                        if i_scale == 0 and s_process_file_addr_64:
                            s_Scale = 64
                        elif i_scale == 1 and s_process_file_addr_16:
                            s_Scale = 16
                        # elif i_scale == 2 and s_process_file_addr_8:
                        #     s_Scale = 8
                        s_file_name = s_process_image_name.split(".")
                        # print("s_file_name[0] : ", s_file_name[0])
                        s_A_frame_data = []
                        if not os.path.isfile(s_file_name[0]+'.csv'):                             # 파일이 없다면
                            with open(s_file_name[0]+'.csv', 'a', newline = '') as file:
                                for col in range(0,s_Scale,1):
                                    insert_row_data = []
                                    for row in range(0,s_Scale,1):
                                        temp_row = [int(F_process_image[col, row])]
                                        insert_row_data.extend(temp_row)
                                    s_A_frame_data.append(insert_row_data)
                                sel_file = csv.writer(file, delimiter = ',')
                                sel_file.writerows(s_A_frame_data)
                        
                        i_A_illuminance[i_scale] = illumination(i_scale, F_process_image)
                    print(s_process_image_name + "Illuminance : ", i_A_illuminance)
                    ###############################################################################################  illuminance csv 저장 안함
        else:
            print("Pass")